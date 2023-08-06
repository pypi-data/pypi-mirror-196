# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

import logging
import re
import os
import csv

import pandas as pd
from pandas import DataFrame
from typing import List, Union, Optional, Dict
from dataclasses import dataclass, field

from iql import q_cache
from iql.bbg_bql.bql_wrapper import (
    BaseBqlQuery,
    execute_bql_str_list_async_q,
    list_to_str,
)
from iql.bbg_bql.bql_datamodel import RawBqlQuery, QueryPipeline
from iql.iqmoql import IqmoQlExtension, register_extension, SubQuery


logger = logging.getLogger(__name__)

_KEYWORD = "bql"

_bql_start_pattern = r"(?si)\(\s*((get)|(let))\s*\("
_bql_pat = re.compile(_bql_start_pattern)

_QUERY_FOR_PATTERN = re.compile(
    r"(?s)(.*for\s*\((.*?)\)\s*)((with.*?)?)\s*((preferences.*)?)"
)


@dataclass
class _IqmoBqlQuery(SubQuery):
    # Extended BQL language to add "iqmo" options
    # such as "splitid" and pivoting
    # Syntax; pivot(id, name)
    # Syntax 2: pivot([id:col2], name)
    bqlquery: BaseBqlQuery = field(init=False)

    def get_query(self) -> str:
        """Overridden, so we can pull a list of ids from an external file"""
        query_base = next(iter(self.options.keys()), None)
        if query_base is None:
            raise ValueError("No BQL query found")

        if "paramfile" in self.options:
            # id_fileparam is a tuple: a string to replace, and a filename to get the values from
            paramname, filename = self.options.get("paramfile")  # type: ignore

            if paramname not in query_base:
                raise ValueError(
                    f"Query doesn't contain the parameter name {paramname} clause, cannot substitute"
                )

            if type(filename) is not str:
                raise ValueError(f"Unexpected type for fileparam: {type(filename)}")

            if os.path.exists(filename):
                logger.info(f"Using ids from {filename}")
                with open(filename, "r") as file:
                    reader = csv.reader(file)
                    values = [v[0] for v in reader]

                    id_list_str = list_to_str(values, quote=True)
                    if paramname not in query_base:
                        raise ValueError(
                            "Query doesn't contain the parameter name {paramname} clause, cannot substitute"
                        )
                    else:
                        newfor = f"[{id_list_str}]"
                        logger.info(f"Replacement for list: {id_list_str}")

                        return query_base.replace(paramname, newfor)

            else:
                raise ValueError(f"idlist does not exist {filename}")
        else:
            return query_base

    def raw_dataframe(self) -> Union[DataFrame, None]:
        return self.bqlquery.dataframe

    def run_outside_batch(self) -> bool:
        return False

    def execute_paramlist(self) -> DataFrame:
        # TODO: Allow this to be batched

        logger.debug("Param list is enabled, splitting query into a two stage pipeline")

        query = self.bqlquery.to_bql_query()

        paramlist: List[str] = self.options.get("paramlist")  # type: ignore
        paramquery: Optional[str] = self.options.get("paramquery")  # type: ignore
        if paramlist is None and paramquery is not None:

            if not isinstance(paramquery, list) and len(paramquery) != 2:
                raise ValueError("paramquery must be a Tuple of (param, 'query')")

            parameter_name = paramquery[0]
            paramquery = paramquery[1]

            df = self.extension.db_connection.sql(paramquery).to_df()  # type: ignore

            parameter_list = df[df.columns[0]].values

        elif paramlist is not None:

            if not isinstance(paramlist, list) and len(paramlist) != 2:
                raise ValueError("paramlist must be a Tuple of (param, [values])")

            parameter_name = paramlist[0]
            parameter_list = paramlist[1]

        if parameter_name not in query:
            raise ValueError(f"{parameter_name} not found in query, nothing to replace")

        queries = []

        for val in parameter_list:

            new_query = query.replace(parameter_name, val)

            logger.debug(f"Creating a raw query for {val}: {new_query}")

            q = RawBqlQuery(new_query)
            queries.append(q)

        execute_bql_str_list_async_q(queries)

        for q in queries:
            if q.dataframe is None:
                raise ValueError("BQL query failed, cannot continue")

        dfs = [q.dataframe for q in queries]

        df = pd.concat(dfs)

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
        prefs_str = match.group(5)
        rest_str = (
            (with_str if with_str is not None else "")
            + " "
            + (prefs_str if prefs_str is not None else "")
        )

        q1_str = f"get (id) for ({for_str}) {rest_str}"
        q1 = RawBqlQuery(q1_str)

        pipeline.add_query(query=q1)

        q2_str = query.replace(for_str, "['$SECURITY']")
        q2 = RawBqlQuery(q2_str)
        pipeline.add_query(query=q2, copy_from_previous=("id", "$SECURITY"))

        pipeline.execute()

        # df = pipeline.dataframe()
        if pipeline.successful():
            self.bqlquery.dataframe = pipeline.dataframe()
            self.bqlquery.execution_status = self.bqlquery.STATUS_COMPLETED

            if self.bqlquery.dataframe is None:
                raise ValueError("Pipeline passed, but dataframe is still None")

            return self.bqlquery.dataframe
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
        # populate_from_cache is called from execute_batch, doesn't need to be run again here
        if self.dataframe is not None:
            return True

        success = self.execute_internal()

        if success:
            df = self.bqlquery.dataframe

            df = self.extension.apply_pandas_operations_prepivot(df, self.options)

            df = self.extension.pivot(df, self.options.get("pivot"))  # type: ignore
            df = self.extension.apply_pandas_operations_postpivot(df, self.options)

            self.dataframe = df
            self.save_to_cache()

            return success
        else:
            allow_failure_opt = self.options.get("allow_failure")
            if allow_failure_opt is None or (
                isinstance(allow_failure_opt, bool) and allow_failure_opt is False
            ):
                return False
            else:

                if isinstance(allow_failure_opt, bool) and allow_failure_opt is True:
                    logger.info(
                        "Query failed, but allow_failure is enabled. Creating an empty dataframe with one id column."
                    )
                    self.dataframe = DataFrame(columns=["id"])
                else:
                    if isinstance(allow_failure_opt, str):
                        cols: List[str] = [allow_failure_opt]
                    else:
                        cols: List[str] = allow_failure_opt  # type: ignore
                    logger.info(
                        f"Query failed, but allow_failure is enabled. Creating an empty dataframe with cols = {cols}"
                    )

                    self.dataframe = DataFrame(columns=cols)
                return True

    def execute_internal(self) -> bool:

        if self.bqlquery.execution_status == BaseBqlQuery.STATUS_FAILURE:
            return False

        if self.bqlquery.execution_status == BaseBqlQuery.STATUS_COMPLETED:
            return True

        if not self.run_outside_batch():
            logger.debug(
                "Query is not executed/cached, this should only occur when a single BQL query is executed"
            )

        working_df = None

        # If it already ran, don't run again
        if not self.bqlquery.execution_status == BaseBqlQuery.STATUS_COMPLETED:
            # logger.info("Not splitting")
            success = self.bqlquery.execute()

            if not success:
                logger.debug(f"Result {success}")
                return False

        # query has passed
        if working_df is None:
            working_df = self.bqlquery.dataframe

        assert working_df is not None

        # validate column names: disabled for now, still a work in progress
        # working_df = self.validate_fix_column_names(working_df)

        self.dataframe = working_df

        return True


@dataclass
class BqlExtension(IqmoQlExtension):
    def create_subqueries(
        self, query: str, name: str, con: object
    ) -> List[_IqmoBqlQuery]:

        # Use the super() implementation, to reuse the paramlist splitting.
        sqs = super().create_subqueries(query, name, con)

        iqs = []
        for sq in sqs:
            iq = _IqmoBqlQuery(
                subquery=sq.subquery, name=sq.name, extension=self, dbcon=con
            )

            bqlstr = iq.get_query()
            q = RawBqlQuery(bqlstr)
            iq.bqlquery = q

            iqs.append(iq)
        return iqs

    def execute_batch(self, subqueries: List[_IqmoBqlQuery]) -> Dict[str, DataFrame]:
        # Caching operates at two levels here:
        # The SubQuery result, and within the bql_wrapper
        # To force a refresh, we'll clear both the subquery and bql raw query
        # cache
        for sq in subqueries:
            sq.populate_from_cache()

        needs_to_be_cleared = [
            q for q in subqueries if not self.allow_cache_read_inner(q)
        ]
        logger.debug(f"Clearing {len(needs_to_be_cleared)}")
        # clear lower-level cache entries
        for q in needs_to_be_cleared:
            q_cache.clear(q.bqlquery.to_bql_query())

        to_run: List[_IqmoBqlQuery] = [
            sq
            for sq in subqueries
            if sq.dataframe is None and not sq.run_outside_batch()
        ]

        queries = [q.bqlquery for q in to_run]

        # We already checked whether its cached AND whether caching is allowed in sq.populate_from_cache
        logger.debug(f"Executing {len(queries)}")
        execute_bql_str_list_async_q(queries)

        completed_dfs = {}
        # Then update the subqueries
        for q in subqueries:
            if q.bqlquery.execution_status == BaseBqlQuery.STATUS_FAILURE:
                raise ValueError(
                    f"BQL SubQuery failed {q.bqlquery.exception_msg}: {q.bqlquery.to_bql_query()}"
                )
            q.execute()
            df = q.dataframe
            completed_dfs[q.name] = df

        return completed_dfs


def execute_bql(query: str, pivot: Optional[str] = None) -> DataFrame:
    """Convenience function for testing, or executing single queries"""

    if _KEYWORD in query:
        raise ValueError(f"Pass raw BQL queries only, don't wrap with {_KEYWORD}(...)")

    elif pivot is not None:
        suffix = f", pivot={pivot}"

    else:
        suffix = ""

    query = f'{_KEYWORD}("{query}"{suffix})'
    extension = BqlExtension(_KEYWORD)

    logger.debug(f"Converted to: {query}")
    sqs = extension.create_subqueries(query, "Anon", con=None)
    sq = sqs[0]

    sq.execute()

    if sq.dataframe is None:
        raise ValueError(f"Unable to execute {sq.subquery}")

    return sq.dataframe


def execute_bql_batch(queries: List[str]) -> Dict[str, Optional[DataFrame]]:
    """Batch executes multiple BQL Queries. Much faster than running serially."""
    extension = BqlExtension(_KEYWORD)

    wrapped_queries = [f'{_KEYWORD}("{q}")' for q in queries]

    iqs = []
    for query in wrapped_queries:
        sqs = extension.create_subqueries(query, "Anon", con=None)
        iqs.extend(sqs)

    extension.execute_batch(iqs)

    return {sq.subquery: sq.dataframe for sq in iqs}


def register(keyword: str):
    global _KEYWORD
    _KEYWORD = keyword
    extension = BqlExtension(keyword=keyword)
    register_extension(extension)
