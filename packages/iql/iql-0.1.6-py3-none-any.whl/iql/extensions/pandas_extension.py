# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

import logging
from dataclasses import dataclass
from pandas import DataFrame
from iql.iqmoql import IqmoQlExtension, register_extension, SubQuery

logger = logging.getLogger(__name__)


@dataclass
class PandasExtension(IqmoQlExtension):
    keyword: str

    def allow_cache_read(self, sq: SubQuery) -> bool:
        # Never cache, because this depends on contents of table
        return False

    def allow_cache_save(self, sq: SubQuery) -> bool:
        return False

    def executeimpl(self, sq: SubQuery) -> DataFrame:
        dfname = sq.options.get("df")
        tablename = sq.options.get("table")
        sql = sq.options.get("sql")

        if dfname is not None:
            query = f"select * from {dfname}"
        elif tablename is not None:
            query = f"select * from {tablename}"
        elif sql is not None:
            query = sql
        else:
            raise ValueError("Must specify one of: df=, table= or sql=")

        # TODO: This is hardcoded for DuckDB. Should rewrite to use iqmoql.DbConnector
        df = sq.dbcon.sql(query).to_df()  # type: ignore
        return df


def register(keyword: str):
    extension = PandasExtension(keyword=keyword)
    register_extension(extension)
