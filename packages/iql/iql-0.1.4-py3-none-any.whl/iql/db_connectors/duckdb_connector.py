# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

import duckdb
import logging
from typing import Dict, List
from pandas import DataFrame
from iql.iqmoql import DatabaseConnector

logger = logging.getLogger(__name__)


class _DuckDbConnector(DatabaseConnector):
    def get_connection(self) -> object:
        """Used for executing multiple queries against the same database"""
        con = duckdb.connect(database=":memory:")
        return con

    def close_connection(self, con):
        try:
            if con is None:
                return

            con.close()
        except Exception:
            logger.exception("Unable to close")

    def execute_query(
        self, con: object, query: str, completed_dfs: Dict[str, DataFrame]
    ) -> List[DataFrame]:
        try:
            # Register each of the dataframes to duckdb, so duckdb can query them
            # Other database might require a "load" or "from_pandas()" step to load these
            # to temporary tables.
            for key, df in completed_dfs.items():
                if df is None:
                    continue
                    # raise ValueError(f"None dataframe for {key}")
                con.register(key, df)  # type: ignore

            r = con.query(query)  # type: ignore
            if r is not None:
                df = r.to_df()
                return [df, *completed_dfs.values()]
            else:
                return []
        except Exception as e:
            logger.exception(f"Error executing SQL DFs: {query}")
            raise e


def getConnector() -> DatabaseConnector:
    return _DuckDbConnector()
