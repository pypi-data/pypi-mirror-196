# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

import logging
import sqlparse
import importlib
import os
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union, Tuple
from pandas import DataFrame
import pandas as pd
from abc import abstractmethod
from iql import q_cache as qc
from iql import options_parser

last_real_name = False


# DB_MODULE is loaded on first call to get_dbmodule()
# Replace this string with another connector prior to first use,
# or set _DBCONNECTOR to None after changing.
DB_MODULE: str = "iql.db_connectors.duckdb_connector"

# Cache Settings
# Use iqmoql.activate_cache() before first execute() to
# ensure settings propogate to individual extensions.
# Infinite in memory cache by default
_CACHE_PERIOD = -1
_USE_FILE_CACHE = False
DEFAULT_EXT_DIRECTORY = None

_EXTENSIONS: Dict[str, "IqmoQlExtension"] = {}
_DBCONNECTOR: Optional["DatabaseConnector"] = None

# Used internally to name the dataframes registered with duckdb
_DFPREFIX: str = "iqmodf"

# Add extensions via register_extension()
# Extensions are loaded on first access, to avoid requiring
# unused dependencies
_KNOWN_EXTENSIONS: Dict[str, str] = {
    "bql": "iql.bbg_bql.bql_extension",
    "s3": "iql.extensions.aws_s3_extension",
    "fred": "iql.extensions.fred_extension",
    "kaggle": "iql.extensions.kaggle_extension",
    "edgar": "iql.extensions.edgar_extension",
    "pandas": "iql.extensions.pandas_extension",
}

logger = logging.getLogger(__name__)


class DatabaseConnector:
    @abstractmethod
    def execute_query(
        self, con: object, query: str, completed_dfs: Dict[str, DataFrame]
    ) -> List[DataFrame]:
        raise ValueError("Implement Me")

    @abstractmethod
    def get_connection(self) -> object:
        raise ValueError("Implement Me")

    @abstractmethod
    def close_connection(self, con):
        raise ValueError("Implement Me")


_lasttoken = None


@dataclass
class IqmoQlExtension:
    keyword: str

    # Determines whether the local cache settings should be used
    # vs  CACHE_PERIOD and
    # USE_FILE_CACHE
    use_default_caching: bool = field(default=True, init=False)
    _cache_period: Optional[int] = field(default=None, init=False)
    _use_file_cache: bool = field(default=False, init=False)

    temp_file_directory: Optional[str] = field(default=None, init=False)

    def allow_cache_read_inner(self, sq: "SubQuery") -> bool:
        """Dont use cached values if nocache=True. Used by individual externals for internal caching."""
        if sq.options.get("nocache") is True:
            return False
        else:
            return True

    def allow_cache_read(self, sq: "SubQuery") -> bool:
        """Dont use cached values"""
        if sq.options.get("nocache") is True:
            return False
        elif sq.options.get("cache") is not None:
            return True
        elif self.get_cache_period() is None:
            return False
        else:
            return True

    def allow_cache_save(self, sq: "SubQuery") -> bool:
        return self.allow_cache_read(sq)

    def get_cache_period(self) -> Optional[int]:
        if self.use_default_caching:
            return _CACHE_PERIOD
        else:
            return self._cache_period

    def use_file_cache(self) -> bool:
        if self.use_default_caching:
            return _USE_FILE_CACHE
        else:
            return self._use_file_cache

    def use_path_replacement(self) -> bool:
        """Some extensions just return a filestring to use instead of the SubQuery, such as the
        S3 Extension. If execute() returns None, then use_path_replacement must be used."""
        return False

    def get_path_replacement(self, query: str) -> Optional[str]:
        """Used for extensions which use a native duckdb extension to access the underlying data"""
        return None

    @abstractmethod
    def executeimpl(self, sq: "SubQuery") -> Optional[DataFrame]:
        raise ValueError("Implement Me")

    def execute(self, sq: "SubQuery") -> Optional[DataFrame]:
        # usage: select * from (verityapi(functionname, targetname)) as verityquery
        # An empty response means no response was needed
        # Internal failure must raise an exception
        if sq.populate_from_cache() and sq.dataframe is not None:
            return sq.dataframe

        logger.debug(f"Executing query {sq.get_query()}")

        df = self.executeimpl(sq)

        if df is None and not self.use_path_replacement():
            raise ValueError("Empty DF, should never reach here")
        else:
            if df is not None:
                pivot_options = sq.options.get("pivot")

                df = self.apply_pandas_operations_prepivot(df, sq.options)

                if pivot_options is not None:
                    df = self.pivot(df, pivot_options)  # type: ignore
                df = self.apply_pandas_operations_postpivot(df, sq.options)

                sq.dataframe = df

                sq.save_to_cache()

                return df

    def execute_batch(self, queries: List["SubQuery"]) -> Dict[str, DataFrame]:
        """Default implementation runs individually, override for functions that can be batched, such as
        BQL's _many functions"""

        completed_dfs = {}
        for query in queries:
            df = self.execute(query)  # type: ignore
            if df is None and not self.use_path_replacement():
                raise ValueError(f"Empty DF, {query.get_query()} failed")
            elif df is None:
                logger.debug("Using path replacement, no DF")
            else:
                query.dataframe = df  # type: ignore
                completed_dfs[query.name] = df

        return completed_dfs

    def create_subqueries(self, query: str, name: str, con: object) -> List["SubQuery"]:
        logger.debug(f"Creating a subquery {name} for {query}")

        sq = SubQuery(extension=self, subquery=query, name=name, dbcon=con)

        # If a paramlist is passed, create one subquery for each value

        if "paramquery" in sq.options:
            paramquery: Tuple[str, str] = sq.options.get("paramquery")  # type: ignore

            if (
                len(paramquery) == 2
                and isinstance(paramquery[0], str)
                and isinstance(paramquery[1], str)
            ):
                parameter_name = paramquery[0]
                param_query = paramquery[1]
                df = con.sql(param_query).to_df()  # type: ignore
                parameter_values = df[df.columns[0]].values
                logger.debug(f"Values {parameter_values}")
            else:
                raise ValueError(f"Invalid options passed to paramquery: {paramquery}")

        elif "paramlist" in sq.options:
            paramlist: Tuple[str, List[str]] = sq.options.get("paramlist")  # type: ignore

            if not isinstance(paramlist, list) and len(paramlist) != 2:
                raise ValueError("paramlist must be a Tuple of (param, [values])")

            parameter_name = paramlist[0]
            parameter_values: List[str] = paramlist[1]
            logger.debug(f"Found paramlist: {parameter_name} => {parameter_values}")

            if parameter_values is None or len(parameter_values) == 0:
                raise ValueError("Empty values passed to paramlist passed")

            if isinstance(parameter_values, str):
                parameter_values = [parameter_values]
        else:
            parameter_name = None
            parameter_values = None  # type: ignore

        if parameter_name is not None:
            assert parameter_values is not None
            sqs: List["SubQuery"] = []
            count = 1

            for v in parameter_values:
                v_query = query.replace(parameter_name, v)

                sq = SubQuery(
                    extension=self, subquery=v_query, name=f"{name}_{count}", dbcon=con
                )
                sqs.append(sq)
                count += 1

            return sqs
        else:
            return [sq]

    def fix_col_ref(self, opt: str, columns: List[str]):
        if opt in columns:
            return opt
        opt_l = opt.lower().strip()
        opt_ci = next((c for c in columns if c.lower() == opt_l), None)

        if opt_ci is None:
            raise ValueError(f"{opt} not in columns: {columns}")

        return opt_ci

    def apply_pandas_operations_postpivot(
        self, working_df, options: Dict[str, object]
    ) -> DataFrame:
        fillna_opt: str = options.get("fillna")  # type: ignore
        if fillna_opt is not None:
            working_df = working_df.fillna(fillna_opt)

        dropna_opt = options.get("dropna")
        if isinstance(dropna_opt, bool) and dropna_opt is True:
            working_df = working_df.dropna()
        elif isinstance(dropna_opt, str):
            working_df = working_df.dropna(subset=[dropna_opt])
        elif isinstance(dropna_opt, list):
            working_df = working_df.dropna(subset=dropna_opt)

        return working_df

    def apply_pandas_operations_prepivot(
        self, working_df, options: Dict[str, object]
    ) -> DataFrame:

        # only drops from the "value" column
        fillna_opt: str = options.get("fillna_pre")  # type: ignore
        if fillna_opt is not None:
            logger.debug(f"Filling NaNs with in value column with {fillna_opt}")
            working_df["value"] = working_df["value"].fillna(fillna_opt)

        dropna_opt = options.get("dropna_pre")
        logger.debug(f"Dropping NA from column {dropna_opt}")
        if isinstance(dropna_opt, bool) and dropna_opt is True:
            working_df = working_df.dropna()
        elif isinstance(dropna_opt, str):
            working_df = working_df.dropna(subset=[dropna_opt])
        elif isinstance(dropna_opt, list):
            working_df = working_df.dropna(subset=dropna_opt)

        return working_df

    def pivot(self, working_df: DataFrame, pivot_option: Union[str, List]) -> DataFrame:
        if pivot_option is None:
            return working_df

        isauto = False
        logger.debug(f"Pivoting by {pivot_option}")
        if isinstance(pivot_option, str):
            if pivot_option.lower() == "none":
                # Pivot disabled / noop
                return working_df
            elif pivot_option.lower() == "auto":
                isauto = True
                index = []
                column = "name"
                value = "value"

                if column not in working_df.columns or value not in working_df.columns:
                    raise ValueError(
                        f"{column} or {value} not found in dataframe columns. Auto should only be used with BQL results."
                    )

                fieldsToCheck = [
                    "id",
                    "orig_ids",
                    "orig_ids:0",
                    "period",
                    "as_of_date",
                    "date",
                ]
                lower_cols = [col.lower() for col in working_df.columns]
                allcols = list(working_df.columns)

                # Case insensitive lookup, but then create an index from the case sensitive names
                for f in fieldsToCheck:
                    if f in lower_cols:
                        index.append(allcols[lower_cols.index(f)])

                if len(index) == 0:
                    index = index[0]
            else:
                raise ValueError("Unexpected pivot setting {pivot_option}")
        elif len(pivot_option) != 2 and len(pivot_option) != 3:
            raise ValueError(f"Unexpected size for pivot options {pivot_option}")
        else:
            index = pivot_option[0]
            column = pivot_option[1]
            value = pivot_option[2] if len(pivot_option) == 3 else "value"

            if index == "auto":
                used_cols = [column.lower(), value.lower()]
                # Use all columns except column and value
                index = [
                    col for col in working_df.columns if col.lower() not in used_cols
                ]
        cols: List[str] = list(working_df.columns)  # type: ignore

        if isinstance(index, list):
            index = [self.fix_col_ref(i, cols) for i in index]
            if len(index) == 1:
                index = index[0]
        else:
            index = self.fix_col_ref(index, cols)

        if isinstance(column, list):
            column = [self.fix_col_ref(i, cols) for i in column]
            if len(column) == 1:
                column = column[0]
        else:
            column = self.fix_col_ref(column, cols)

        if isinstance(value, list):
            value = [self.fix_col_ref(i, cols) for i in value]
            if len(value) == 1:
                value = value[0]
        else:
            value = self.fix_col_ref(value, cols)

        if isinstance(column, list):
            # Needed to allow pivoting by datetime columns
            for col in column:
                if pd.api.types.is_datetime64_any_dtype(working_df[col]):
                    working_df[col] = working_df[col].dt.strftime("%Y-%m-%d")

        logger.debug(f"Pivot index {index} columns {column} values {value}")

        try:
            working_df = working_df.pivot(
                index=index,
                columns=column,
                values=value,
            )
        except Exception as e:
            if not isauto:
                raise e
            else:
                logger.debug("Failed to auto pivot, trying a wider pivot")
                index = [col for col in working_df.columns if col.lower() not in [column.lower(), value.lower()]]  # type: ignore

                working_df = working_df.pivot(
                    index=index,
                    columns=column,
                    values=value,
                )

        working_df = working_df.reset_index()

        if isinstance(column, list) and len(column) > 1:
            # Flatten multicolumn indices
            working_df.columns = [
                "_".join(str(col) if type(col) == int else col)
                for col in working_df.columns.values
            ]

        # Clean columns
        renames = {}
        for col in working_df.columns:
            # assert isinstance(col, str)
            colname = col
            newcol = (
                str(colname)
                .replace("#", "")
                .replace("(", "")
                .replace(")", "")
                .replace(" ", "_")
            )
            newcol = newcol.strip("_")
            if col != newcol:
                # columns can't have #, ( or ) symbols
                # logger.debug(f"Replacing {col} with {newcol}")
                renames[col] = newcol

        if len(renames) > 0:
            working_df = working_df.rename(columns=renames)

        return working_df


@dataclass
class SubQuery:
    extension: IqmoQlExtension
    subquery: str
    name: str
    dbcon: object
    dataframe: Optional[DataFrame] = field(default=None, init=False)

    options: Dict[str, object] = field(default_factory=dict, init=False)

    def get_query(self) -> str:
        """Returns the first parameter to:
        keyword(query, *params)"""
        if len(self.options) == 0:
            raise ValueError("Options not properly passed or parsed")

        query = next(iter(self.options.keys()))
        return query

    def __post_init__(self):
        logger.debug(f"Parsing subquery for {self.subquery}")
        self.options: Dict[str, object] = options_parser.options_to_list(self.subquery)
        logger.debug(f"Options: {self.options}")

    def populate_from_cache(self) -> bool:
        """Returns cached value if it's available"""
        cache_val = self.subquery

        logger.debug(f"Checking cache for {cache_val}, {type(self)}")
        if not self.extension.allow_cache_read(self):
            return False

        df = qc.get(key=cache_val, use_file_cache=self.extension.use_file_cache())
        if df is not None:
            logger.debug("Using cached SubQuery")
            self.dataframe = df  # type: ignore
            return True
        else:
            logger.debug("Not found in cache")
            return False

    def save_to_cache(self):
        if not self.extension.allow_cache_save(self):
            return

        cache_period = self.extension.get_cache_period()

        cache_override = self.options.get("cache")
        if cache_override is not None:
            if isinstance(cache_override, int):
                cache_period = cache_override
            else:
                raise ValueError(f"Invalid cache value passed: {cache_override}")

        cache_val = self.subquery

        logger.debug(
            f"Saving to cache {cache_val} {self.extension.get_cache_period()} override {cache_override}"
        )

        if self.dataframe is not None:
            qc.save(
                key=cache_val,
                o=self.dataframe,
                duration_seconds=cache_period,
                use_file_cache=self.extension.use_file_cache(),
            )


class IqmoQueryContainer:
    # This is used so we can run the bql_queries as an async batch, separate from processing the results.
    orig_query: str
    query: str
    subqueries: List[SubQuery]
    con: object

    def _extract_replacements(self) -> List[SubQuery]:
        """Extensions are functions within the SQL, which will be replaced by dataframes
        Example - assuming bql is a registered extension:
            select * from bql("....") as q1
        will be replaced with:
            select * from df1 as q1

        And "bql("....")" will be executed via the bql_extension.

        Returns: ( modified_query , Dict[name, Subquery] )
        """

        extension_keywords = list_extensions()

        if len(extension_keywords) == 0:
            raise ValueError("No EXTENSIONS defined")

        # remove comments from query
        query = self.query
        query = sqlparse.format(query, strip_comments=True).strip()

        replacements: Dict[str, str] = {}
        subqueries: List[SubQuery] = []

        def process_node(token, level: int = 0):
            global last_real_name
            real_name = token.get_real_name()
            this_last_real_name = last_real_name
            last_real_name = real_name
            # alias = token.get_alias()
            value = token.value
            useThis = False
            name = f"{_DFPREFIX}{len(replacements) + 1}"
            if (
                real_name is None
                and type(token) == sqlparse.sql.Parenthesis
                and this_last_real_name in extension_keywords
            ):
                if re.match(rf"(?s)[\(\s]+{real_name}.*", value) is not None:
                    # WITH alias as bql(....)
                    useThis = True
                    logger.debug(
                        "real name is None, but we're in a paren and last_real_name was a keyword"
                    )

            if real_name in extension_keywords or useThis:

                if real_name is None and this_last_real_name in extension_keywords:
                    real_name = this_last_real_name
                    value = f"{real_name}{value}"

                # remove the prefix (abc as ...), for WITHs
                value = value[value.index(real_name) :]
                # remove any suffix (...) as abc, for SELECTs
                if ")" in value:
                    value = value[: value.rindex(")") + 1]

                logger.debug(f"Found extension {real_name}, value: {value}")
                global _lasttoken
                _lasttoken = token
                if str(real_name.strip()) == str(
                    value.strip()
                ):  # in some cases, the () section is parsed as the next token
                    logger.debug("Skip this, the next paren is what we need")
                    return

                extension = get_extension(real_name)

                sqs: List[SubQuery] = extension.create_subqueries(value, name, self.con)

                subqueries.extend(sqs)

                if extension.use_path_replacement():
                    names = [
                        sq.extension.get_path_replacement(sq.get_query()) for sq in sqs
                    ]
                else:
                    names = [sq.name for sq in sqs]

                querystrings = [f"(select * from {i})" for i in names]
                if len(querystrings) == 1:
                    result = querystrings[0]
                else:
                    # SQL Union of the results
                    # '((select * from a) union (select * from b) union (select * from c))'
                    result = " union ".join(querystrings)
                    result = f"({result})"

                replacements[value] = result

                return
            for t in token.get_sublists():
                process_node(t, level + 1)

        for s in sqlparse.parse(query):
            process_node(s)

        for old, new in replacements.items():
            query = query.replace(old, new)

        self.query = query

        logger.debug(self.query)
        return subqueries

    def __init__(self, query: str, con: Optional[object]):
        self.orig_query = query
        self.query = query
        self.con = con

        self.subqueries = self._extract_replacements()
        # Sanity checks. These don't take into account escaping or quoting, so they're just warnings.
        if query.count("(") != query.count(")"):
            logger.warning("Left and Right Paren counts aren't equal")

        if query.count("'") % 2 != 0:
            logger.warning("Uneven number of single quotes")

        if query.count('"') % 2 != 0:
            logger.warning("Uneven number of double quotes")

    def get_subqueries_by_extension(self, keyword: str) -> List[SubQuery]:
        results: List[SubQuery] = []
        results = [s for s in self.subqueries if s.extension.keyword == keyword]

        return results

    def execute(self) -> List[DataFrame]:
        # Execute the subqueries
        if _DBCONNECTOR is None:
            raise ValueError("DBConnector Not Set")

        if self.con is None:
            con = _DBCONNECTOR.get_connection()
        else:
            con = self.con
        try:
            completed_dfs: Dict[str, DataFrame] = {}

            for keyword, e in _EXTENSIONS.items():
                # db_connection is used by Pandas extension
                # TODO: This isn't thread safe, since extensions are reused

                sqs: List[SubQuery] = self.get_subqueries_by_extension(keyword)
                e_dfs = e.execute_batch(sqs)

                completed_dfs.update(e_dfs)

            return _DBCONNECTOR.execute_query(
                con=con, query=self.query, completed_dfs=completed_dfs
            )
        finally:
            if self.con is None:
                # If connection is created in this function
                con.close()  # type: ignore


def execute(
    query: str, keyword: Optional[str] = None, con: Optional[object] = None
) -> Optional[DataFrame]:
    """Executes the given SQL query. Keyword is only used to run a single subquery without SQL."""

    fthree = query.strip(" \t\n\r").lower()[0:3]
    if fthree in ["let", "get"]:
        keyword = "bql"

    if keyword is not None:
        # Special convenience case if you're running just a single subquery
        query = escaped = query.replace(
            '"', '\\"'
        )  # not perfect, doesn't handled escaped
        query = f'{keyword}("{escaped}")'

    # If passed a connection, don't close it.
    close_connection = con is None

    if con is None:
        get_dbconnector()

        if _DBCONNECTOR is None:
            raise ValueError("DBConnector Not Set")

        con = _DBCONNECTOR.get_connection()

    try:
        dfs = None
        # A single query might contain multiple SQL statements. Parse them out and iterate:
        for statement in sqlparse.parse(query):
            singlequery = statement.value.strip(";")
            iqc = IqmoQueryContainer(query=singlequery, con=con)

            # Run each statement, but only keep the results from the last one
            dfs = iqc.execute()

        # The first result is the query result. The other df's are for debugging purposes
        # If it's not a select, there won't be response, such as in a COPY (..) TO

        if dfs is None:
            return None

        return dfs[0] if len(dfs) > 0 else None

    finally:
        if close_connection:

            if _DBCONNECTOR is None:
                raise ValueError("DBConnector Not Set")

            _DBCONNECTOR.close_connection(con)


def get_dbconnector() -> DatabaseConnector:
    global _DBCONNECTOR
    if _DBCONNECTOR is None:
        # Initializes only on first reference
        module = importlib.import_module(DB_MODULE)
        _DBCONNECTOR = module.getConnector()

    if _DBCONNECTOR is None:
        raise ValueError("Failure initializing _DBCONNECTOR")
    return _DBCONNECTOR


def register_extension(e: IqmoQlExtension):
    _EXTENSIONS[e.keyword] = e
    if e.keyword not in _KNOWN_EXTENSIONS.keys():
        _KNOWN_EXTENSIONS[e.keyword] = e.keyword

    if e.temp_file_directory is None:
        e.temp_file_directory = DEFAULT_EXT_DIRECTORY


def list_extensions() -> List[str]:
    return list(_KNOWN_EXTENSIONS.keys())


def get_extension(keyword: str) -> "IqmoQlExtension":
    """Loads extension on first use"""
    if keyword in _EXTENSIONS:
        return _EXTENSIONS[keyword]
    elif keyword not in _KNOWN_EXTENSIONS.keys():
        raise ValueError(f"Unknown Extension {keyword}")
    else:
        # Dynamically load extensions on first use
        # This avoids requiring installation of packages that
        # aren't needed
        classname = _KNOWN_EXTENSIONS[keyword]
        module = importlib.import_module(classname)
        module.register(keyword)

        return _EXTENSIONS[keyword]


def activate_cache(
    duration_seconds: Optional[int] = -1, cache_directory: Optional[str] = None
):
    """
    Must be called before extensions are initialized (on first use)
    duration_seconds: None (Disabled), -1 (Infinite), int (Seconds)
    file_directory: None (no file cache), string (output directory)
    """
    global _CACHE_PERIOD
    global _USE_FILE_CACHE
    global _DEFAULT_EXT_DIRECTORY

    _CACHE_PERIOD = duration_seconds
    if cache_directory is None:
        _USE_FILE_CACHE = False
    else:
        _USE_FILE_CACHE = True
        if not os.path.exists(cache_directory):
            raise ValueError(f"cache_directory {cache_directory} does not exist")

        _DEFAULT_EXT_DIRECTORY = cache_directory
        qc.activate_file_cache(cache_directory)
