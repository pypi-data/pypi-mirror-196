# Copyright (C) 2023, IQMO Corporation [support@iqmo.com]
# All Rights Reserved

import logging
import sqlparse
import re
from dataclasses import dataclass, field
from pandas import DataFrame
from typing import List, Dict, Optional
from abc import abstractmethod
import initializer as init

import q_cache as qc

CACHE_PERIOD = None # -1 to disable, None for infinite, otherwise # of seconds
USE_FILE_CACHE = True # Use a file cache to persist the cache across kernel restarts

_EXTENSIONS: Dict[str, 'IqmoQlExtension'] = {}
_DBCONNECTOR: Optional['DatabaseConnector'] = None
_DFPREFIX: str = 'df'

logger = logging.getLogger(__name__)

class DatabaseConnector():

    @abstractmethod
    def execute_query(self, query: str, completed_dfs: Dict[str, DataFrame]) -> List[DataFrame]:
        raise ValueError("Implement Me")
    
@dataclass
class IqmoQlExtension():
    keyword: str

    def strip_keyword_wrapper(self, query: str) -> str:
        m = re.match(rf"(?si)\s*{self.keyword}\((.*)\)\s*", query)
        if m is None:
            raise ValueError(f"Unexpected prefix: {query}")
        else:
            query_only = m.group(1)

            query_only = query_only.strip("'")

            return query_only

    @abstractmethod
    def executeimpl(self, option: str) -> Optional[DataFrame]:
        raise ValueError("Implement Me")
    
    def execute(self, sq: 'SubQuery') -> Optional[DataFrame]:
        # usage: select * from (verityapi(functionname, targetname)) as verityquery
        # An empty response means no response was needed
        # Internal failure must raise an exception
        if sq.populate_from_cache() and sq.dataframe is not None:
            return sq.dataframe

        query_string = self.strip_keyword_wrapper(sq.subquery)

        logger.info("Executing query {querystr}")

        df = self.executeimpl(query_string)
        if df is None:
            return None
        
        sq.dataframe=df
        sq.save_to_cache()
        return sq.dataframe

    def execute_batch(self, queries: List[object]):
        """Default implementation runs individually, override for functions that can be batched, such as 
        BQL's _many functions"""
        for query in queries:
            df = execute(query.subquery) # type: ignore
            query.dataframe = df # type: ignore

    @abstractmethod
    def create_subquery(self, query: str, name: str) -> 'SubQuery':
        sq = SubQuery(extension=self, subquery=query, name=name)

        return sq
    
@dataclass
class SubQuery:
    extension: IqmoQlExtension
    subquery: str
    name: str 
    dataframe: Optional[DataFrame] = field(default=None, init=False)

    def populate_from_cache(self) -> bool:
        df = qc.get(self.subquery, use_file_cache=USE_FILE_CACHE)
        if df is not None:
            logger.info("Found in cache")
            self.dataframe = df # type: ignore
            return True
        else:
            logger.info("Not found in cache")
            return False

    def save_to_cache(self):
        logger.info("Saving to cache")
        if self.dataframe is not None:
            qc.save(self.subquery, self.dataframe, CACHE_PERIOD, use_file_cache=USE_FILE_CACHE)

    def execute(self) -> bool:
        df = self.extension.execute(self)
        if df is None:
            return False
        else:
            self.dataframe = df
            return True

class IqmoQueryContainer:
    #This is used so we can run the bql_queries as an async batch, separate from processing the results.
    orig_query: str
    query: str
    subqueries: List[SubQuery]

    #current_date = date.today()
    #anchor_date = current_date - relativedelta(years=2)
    #date_str = anchor_date.strftime("%Y-%m-%d")
    def _extract_replacements(self, extensions: Dict[str, IqmoQlExtension]) -> List[SubQuery]:
        """Extensions are functions within the SQL, which will be replaced by dataframes
        Example - assuming query_bql is a registered extension: 
            select * from query_bql(....) as q1
        will be replaced with:
            select * from df1 as q1

        And "query_bql(....)" will be executed via the query_bql extension.

        Returns: ( modified_query , Dict[name, Subquery] )
        """

        if len(extensions) == 0:
            raise ValueError("No EXTENSIONS defined")

        if _DBCONNECTOR is None:
            raise ValueError("No DBCONNECTOR")

        extension_keywords = extensions.keys()

        # remove comments from query
        query = self.query
        query=sqlparse.format(query, strip_comments=True).strip()

        replacements: Dict[str, str] = {}
        subqueries: List[SubQuery] = []
        def process_node(token, level: int = 0):
            real_name = token.get_real_name()
            #alias = token.get_alias()
            value = token.value
            name = f"{_DFPREFIX}{len(replacements) + 1}"

            logger.debug(f"{token.ttype} - {token.get_name()} - {token.value} - {type(token)} - {token.get_real_name()}")
            if  real_name in extension_keywords:
                # WITH alias as query_bql(....)
                
                # remove the prefix (abc as ...), for WITHs
                value = value[value.index(real_name):]
                # remove any suffix (...) as abc, for SELECTs
                if ")" in value:
                    value = value[:value.rindex(")") + 1]
                sq = extensions[real_name].create_subquery(value, name)
                subqueries.append(sq)
                replacements[value] = f"(select * from {name})"
                return 
                
            for t in token.get_sublists():
                process_node(t, level + 1)

        for s in sqlparse.parse(query):
            process_node(s)
        
        for old, new in replacements.items():
            query = query.replace(old, new)

        self.query = query

        logger.info(self.query)
        return subqueries

    def __init__(self, query: str, extensions: Dict[str, IqmoQlExtension]):
        self.orig_query = query
        self.query = query
        self.subqueries = self._extract_replacements(extensions)

        # Sanity checks. These don't take into account escaping or quoting, so they're just warnings. 
        if query.count("(") != query.count(")"):
            logger.warning("Left and Right Paren counts aren't equal")
         
        if query.count("'") % 2 != 0:
            logger.warning("Uneven number of single quotes")
        
        if query.count('"') % 2 != 0:
            logger.warning("Uneven number of double quotes")
            
    def get_subqueries_by_keyword(self, keyword: str) -> List[SubQuery]:
        return [s for s in self.subqueries if s.extension.keyword == keyword]

    def execute(self) -> List[DataFrame]:
        if _DBCONNECTOR is None:
            raise ValueError("DBConnector Not Set")
        # Execute the subqueries
        completed_dfs: Dict[str, DataFrame] = {}
        for sq in self.subqueries:
            success = sq.execute()
            if not success or sq.dataframe is None:
                raise ValueError(f"Failure executing subquery: {sq.subquery}")
            
            completed_dfs[sq.name] = sq.dataframe

        # logger.info(completed_dfs)
        return _DBCONNECTOR.execute_query(self.query, completed_dfs)


def execute(query: str) -> DataFrame:
    """Executes the given query,"""
    if re.match(r"(?si)((get)|(let)).*", query.strip()) != None:
        # If this is a raw BQL query, wrap with query_bql for consistency
        query = f"query_bql({query})"

    iqc = IqmoQueryContainer(query, _EXTENSIONS)
    
    dfs = iqc.execute()
    # The first result is the query result. The other df's are for debugging purposes
    return dfs[0]


def register_extension(e: IqmoQlExtension):
    _EXTENSIONS[e.keyword] = e

def list_extensions():
    for e in _EXTENSIONS.keys():
        print(e)
