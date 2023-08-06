import logging
import re
import ast
import pandas as pd
from pandas import DataFrame
from typing import List, Union, Optional, Dict

from dataclasses import dataclass, field
from bbg_bql.bql_wrapper import BaseBqlQuery, execute_bql_str_list_async_q
from bbg_bql.bql_datamodel import RawBqlQuery, BqlQuery, QueryPipeline
from iqmoql import IqmoQlExtension, register_extension, SubQuery


logger = logging.getLogger(__name__)

bql_start_pattern = r"(?si)\(\s*((get)|(let))\s*\("
bql_pat = re.compile(bql_start_pattern)

_QUERY_FOR_PATTERN = re.compile(r"(?s)(.*for\s*\((.*?)\)\s*)((with.*?)?)\s*((preferences.*)?)")
_BEFORE_AS_PATTERN = re.compile("(?si)(.*?)\\s+as\\s+(#[\\d\\w_]+)")
_QUERY_BQL = re.compile(r"(?s)(.*)(iqmo\((.*)\)\s*)")
_KNOWN_OPTIONS = ["dropna", "splitids", "pivot", "allow_failure", "paramlist"]

EXTENSION_KEYWORD = "query_bql"

@dataclass
class _IqmoBqlQuery(SubQuery):
    # Extended BQL language to add "iqmo" options
    # such as "splitid" and pivoting
    # Syntax; pivot(id, name)
    # Syntax 2: pivot([id:col2], name)
    bqlquery: BaseBqlQuery

    # Available Options:
    # splitids: bool
    options: Dict[str, str] = field(default_factory=dict)

    def raw_dataframe(self) -> Union[DataFrame, None]:
        return self.bqlquery.dataframe

    def fix_col_ref(self, opt: str, columns: List[str]):
        if opt in columns:
            return opt
        opt_l = opt.lower().strip()
        opt_ci = next((c for c in columns if c.lower() == opt_l), None)

        if opt_ci is None:
            raise ValueError(f"{opt} not in columns: {columns}")

        return opt_ci

    def _convert_to_list(self, input: str, columns: List[str]) -> List[str]:
        index = input
        if isinstance(index, str) and (index[0] == "[" or index[0] == "("):
            index = index[1:-1]
            if "," in index:
                index = index.split(",")

            indexnew: List[str] = []
            for i in index:
                fixedi = self.fix_col_ref(i, columns)
                indexnew.append(fixedi)

            return indexnew
        else:
            fixedi = self.fix_col_ref(index, columns)
            return [fixedi]
    
    def pivot_using_options(
        self, working_df: DataFrame, pivot_option: str
    ) -> DataFrame:

        if pivot_option.lower() == "none":
            # Pivot disabled / noop
            return working_df
        elif pivot_option.lower() == "auto":
            index = []
            column = "name"
            value = "value"

            if "ID" in working_df.columns:
                index.append("ID")

            if "id" in working_df.columns:
                index.append("id")

            if "ORIG_IDS" in working_df.columns:
                index.append("ORIG_IDS")

            if "ORIG_IDS:0" in working_df.columns:
                index.append("ORIG_IDS:0")

            if "PERIOD" in working_df.columns:
                index.append("PERIOD")

            if "AS_OF_DATE" in working_df.columns:
                index.append("AS_OF_DATE")

            if "DATE" in working_df.columns:
                index.append("DATE")

            if len(index) == 0:
                index = index[0]

        elif pivot_option[0] == "(" and pivot_option[-1] == ")":
            # Strip leading/trailing parens
            pivot_option = pivot_option[1:-1]

            po_s = split_options(pivot_option)
            #po_s = pivot_option.split(",")

            logger.info(f"After splitting: {po_s}")
            if len(po_s) == 2:
                index = po_s[0].strip()
                column = po_s[1].strip()
                value = "value"
            elif len(po_s) == 3:
                index = po_s[0].strip()
                column = po_s[1].strip()
                value = po_s[2].strip()
            else:
                raise ValueError(
                    f"Unexpected number of options for pivot: {pivot_option}"
                )
        else:
            raise ValueError(
                f"Pivot option doesn't begin and end with parens: {pivot_option}"
            )

        cols: List[str] = list(working_df.columns)  # type: ignore

        # convert index to a list 
        if isinstance(index, str):
            index = self._convert_to_list(index, cols)
        
        # convert columns to a list
        if isinstance(column, str):
            column = self._convert_to_list(column, cols)

        if isinstance(index, str):
            index = self.fix_col_ref(index, cols)

        if isinstance(column, str):
            column = self.fix_col_ref(column, cols)

        if value not in cols:
            value = self.fix_col_ref(value, cols)

        logger.info(f"Pivot index {index} columns {column} values {value}")
        working_df = working_df.pivot(
            index=index[0] if isinstance(index, list) and len(index)==1 else index,
            columns=column[0] if isinstance(column, list) and len(column)==1 else column,
            values=value,
        )
        working_df = working_df.reset_index()

        if isinstance(column, list) and len(column)>1:
            working_df.columns = ['_'.join(col) for col in working_df.columns.values]

        return working_df


    def execute_paramlist(self) -> DataFrame:
        # TODO: Allow this to be batched
        paramlist_opt: str = self.options.get("paramlist") # type: ignore
        if paramlist_opt is None:
            raise ValueError("No paramlist found")
        
        parameter_name = paramlist_opt[:paramlist_opt.index("[")]
        parameter_list_s = paramlist_opt[paramlist_opt.index("["):]
        parameter_list = ast.literal_eval(parameter_list_s)
        logger.info(f"{parameter_name} - {parameter_list}")


        logger.debug("Param list is enabled, splitting query into a two stage pipeline")

        # Extract For Clause
        query = self.bqlquery.to_bql_query()

        match = _QUERY_FOR_PATTERN.fullmatch(query)

        if match is None:
            raise ValueError(f"Could not extract FOR clause from {query}")
        
        before_with = match.group(1)
        #for_str = match.group(2)

        with_str = match.group(3)
        preferences_str = match.group(4)
        queries = []
        for val in parameter_list:
                
            #q1_str = f"get (id) for ({for_str}) {rest_str}"

            if with_str is None:
                with_str = f"with ({parameter_name} = {val})"
                new_query = f"{before_with} {with_str} {preferences_str}"
            else:
                if parameter_name in with_str:
                    raise ValueError(f"{parameter_name} is already in the WITH clause: {with_str}")

                new_with_str = with_str.strip()
                new_with_str = new_with_str[:-1] # take off trailing )
                new_with_str = f"{new_with_str}, {parameter_name}='{val}')"
                new_query= query.replace(with_str, new_with_str)

            logger.info(f"Creating a raw query for {val}: {new_query}")

            q = RawBqlQuery(new_query)
            queries.append(q)

        execute_bql_str_list_async_q(queries)

        for q in queries:
            if q.dataframe is None:
                raise ValueError("BQL query failed, cannot continue")
            
        dfs = [q.dataframe for q in queries]
         
        
        df=pd.concat(dfs)

        self.bqlquery.dataframe = df
        return df
        
    def execute_split(self) -> DataFrame:
        # TODO: Allow this to be batched
        logger.debug("Split is enabled, splitting query into a two stage pipeline")
        pipeline = QueryPipeline()

        # Extract For Clause
        query = self.bqlquery.to_bql_query()

        match = _QUERY_FOR_PATTERN.fullmatch(query)

        if match is None:
            raise ValueError(f"Could not extract FOR clause from {query}")
        for_str = match.group(2)
        with_str = match.group(3) 
        prefs_str = match.group(4)
        rest_str = (with_str if with_str is not None else "") + " " + (prefs_str if prefs_str is not None else "")

        q1_str = f"get (id) for ({for_str}) {rest_str}"
        q1 = RawBqlQuery(q1_str)

        pipeline.add_query(query=q1)

        q2_str = query.replace(for_str, "['$SECURITY']")
        q2 = RawBqlQuery(q2_str)
        pipeline.add_query(query=q2, copy_from_previous=("id", "$SECURITY"))

        pipeline.execute()

        df = self.bqlquery.dataframe
        if pipeline.successful() and df is not None:
            self.bqlquery.dataframe = pipeline.dataframe()
            self.bqlquery.execution_status = self.bqlquery.STATUS_COMPLETED
            return df
        else:
            self.bqlquery.execution_status = self.bqlquery.STATUS_FAILURE
            raise ValueError("Failure in execution")
    # detects everything before "(.*) as #..."

    def validate_fix_column_names(self, df) -> DataFrame:
        # BQL does two annoying things:
        # 1. It drops duplicate columns silently, even if the duplicates are desired or slightly different.
        # This detects this case, and throws an exception to force the query writer to handle it.
        # 2. It sometimes ignores the "alias", so this will re-insert the alias if needed

        if len(df) == 0:
            return df

        cols_returned = list(df["name"].unique())
        cols_expected = self.bqlquery.get_fields()
        if len(cols_returned) != len(cols_expected):

            raise ValueError(
                f"""Unexpected number of columns returned. Expected {len(cols_expected)}, 
                got {len(cols_returned)}. Got: {df['name'].unique()}, expected {cols_expected}"""
            )

        if (
            True
        ):  # We expect that the columns match 1 to 1, so make sure the columns match the "as" of cols_expected
            for i in range(len(cols_returned)):
                r = cols_returned[i]
                e = cols_expected[i]

                if r == e or re.sub(r"\s+", "", r) == e:
                    # it's equal, or without spaces, it's equal
                    continue

                if r[0] == "#":
                    # this is an aliased field
                    continue

                raise ValueError(f"Expected {e}, got {r}")

        return df

    def execute(self) -> bool:
        self.populate_from_cache()
        
        if self.dataframe is not None:
            return True
        
        success = self.execute_internal()
        if success:
            self.save_to_cache()

            return success
        else:
            allow_failure_opt = self.options.get("allow_failure")
            if allow_failure_opt is None or allow_failure_opt.lower() == "false":
                return False
            else:

                if allow_failure_opt.lower() == "true":
                    logger.info(
                        "Query failed, but allow_failure is enabled. Creating an empty dataframe with one id column."
                    )

                    self.dataframe = DataFrame(columns=["id"])
                else:
                    cols = allow_failure_opt.split(",")
                    logger.info(
                        f"Query failed, but allow_failure is enabled. Creating an empty dataframe with cols = {cols}"
                    )

                    self.dataframe = DataFrame(columns=cols)
                return True

    def execute_internal(self) -> bool:
        
        if self.bqlquery.execution_status == BaseBqlQuery.STATUS_FAILURE:
            return False

        

        splitopt = self.options.get("splitids")
        paramlist = self.options.get("paramlist")

        if splitopt is not None and paramlist is not None:
            raise ValueError("Can't use splitopt and paramlist at the same time")
        
        working_df = None
        if paramlist is not None:
            logger.info("Executing each item in paramlist")
            working_df = self.execute_paramlist()
            if working_df is None:
                return False
        elif splitopt is not None and splitopt.lower() == "true":
            # logger.info("Splitting")
            working_df = self.execute_split()
            if working_df is None:
                return False
        else:
            # If it already ran, don't run again
            if not self.bqlquery.execution_status == BaseBqlQuery.STATUS_COMPLETED:
                # logger.info("Not splitting")
                success = self.bqlquery.execute()

                if not success:
                    logger.info(f"Result {success}")
                    return False

        # query has passed
        if working_df is None:
            working_df = self.bqlquery.dataframe
            
        assert working_df is not None

        dropna_opt = self.options.get("dropna")
        if dropna_opt is not None:
            logger.info(f"Dropping NA from column {dropna_opt}")
            working_df.dropna(subset=[dropna_opt], inplace=True)

        # validate column names: disabled for now, still a work in progress
        # working_df = self.validate_fix_column_names(working_df)

        pivot_option = self.options.get("pivot")
        if pivot_option is not None:
            working_df = self.pivot_using_options(working_df, pivot_option)

        renames = {}
        for col in working_df.columns:
            assert isinstance(col, str)

            newcol = col.replace("#", "").replace("(", "").replace(")", "").replace(" ", "_")
            newcol=newcol.strip("_")
            if col != newcol:
                # columns can't have #, ( or ) symbols
                logger.info(f"Replacing {col} with {newcol}")
                renames[col] = newcol
        if len(renames) > 0:
            working_df = working_df.rename(columns=renames)

        self.dataframe = working_df

        return True

def split_options(text: str) -> List[str]:
    
    paren_depth = 0
    last = 0
    results = []
    for i in range(len(text)):
        c=text[i]
        if c == "," and paren_depth == 0:
            results.append(text[last:i].strip())
            last = i+1
        elif c == "(" or c == "[":
            paren_depth += 1
        elif c == ")" or c == "]":
            paren_depth -= 1

    if len(text)!=last:
        results.append(text[last:len(text)].strip())

    return results

@dataclass
class BqlExtension(IqmoQlExtension):
    keyword: str = EXTENSION_KEYWORD

    def _convert_bqlstr_to_iqmobql(self, full_query: str, name: str) -> _IqmoBqlQuery:
        # Extract the query from the function: query_bql(...)
        bqlstr = self.strip_keyword_wrapper(full_query)

        match = _QUERY_BQL.fullmatch(bqlstr)

        if match is None:
            # Query has no iqmo clause
            q = RawBqlQuery(bqlstr)
            iq = _IqmoBqlQuery(bqlquery=q, subquery=full_query,  name=name, extension=self)
            return iq
        else:
            logger.debug("Has Iqmo Options")
            # Extract options
            bqlstr_only = match.group(1)
            iqmo_options = match.group(3)

            q = RawBqlQuery(bqlstr_only.strip())
            iq = _IqmoBqlQuery(bqlquery=q, subquery=full_query,  name=name, extension=self)

            logger.debug(iqmo_options)

            options = split_options(iqmo_options)
            
            for option in options:
                if "=" not in option:
                    raise ValueError(f"Option doesn't contain an =: {option}")

                pos = option.index("=")
                key = option[:pos]
                value = option[pos+1:]
                key=key.strip()
                value=value.strip()
                
                key = key.lower()
                # for key, value, *ignore in _OPTIONS_PAT.findall(iqmo_options):
                if key not in _KNOWN_OPTIONS:
                    raise ValueError(f"Unknown option {key}")
                logger.info(f"Setting query option {key} {value}")
                iq.options[key] = value

            return iq
    
    def create_subquery(self, query: str, name: str) -> _IqmoBqlQuery:
        sq = self._convert_bqlstr_to_iqmobql(query, name)
        return sq
    
    def execute_batch(self, subqueries: List[_IqmoBqlQuery]):
        # Run the underlying queries
        # First checks to see if they have a cached result
        # Then executes as a batch in the BQL layer

        for sq in subqueries:
            sq.populate_from_cache()
        
        not_cached: List[_IqmoBqlQuery] = [sq for sq in subqueries if sq.dataframe is None]
        
        queries = [q.bqlquery for q in not_cached]
        execute_bql_str_list_async_q(queries)

        # Then update the subqueries
        for q in subqueries:
            q.execute()

def register_extension_bql():
    extension = BqlExtension()
    register_extension(extension)

def execute_bql(query: str, pivot: Optional[str] = None) -> DataFrame:
    """Convenience function for testing, or executing single queries"""

    if EXTENSION_KEYWORD in query:
        raise ValueError(f"Pass raw BQL queries only, don't wrap with {EXTENSION_KEYWORD}(...)")
    
    if pivot is not None and "iqmo" in query:
        raise ValueError("iqmo(...) defined, but pivot parameters also passed. Use one or the other")
    
    elif pivot is not None:
        suffix = f" iqmo(pivot={pivot})"
        query = query + suffix

    query = f"{EXTENSION_KEYWORD}({query})"
    extension = BqlExtension()

    logger.info(f"Converted to: {query}")
    sq: SubQuery = extension._convert_bqlstr_to_iqmobql(query, "Anon")
    sq.execute()

    if sq.dataframe is None:
        raise ValueError(f"Unable to execute {sq.subquery}")
    
    return sq.dataframe

def execute_bql_batch(queries: List[str]) -> Dict[str, Optional[DataFrame]]:
    """Batch executes multiple BQL Queries. Much faster than running serially. """
    extension = BqlExtension()

    wrapped_queries = [f"{EXTENSION_KEYWORD}({q})" for q in queries]
    subqueries = [extension._convert_bqlstr_to_iqmobql(query, "Anon") for query in wrapped_queries]
    
    extension.execute_batch(subqueries)

    return {sq.subquery: sq.dataframe for sq in subqueries}