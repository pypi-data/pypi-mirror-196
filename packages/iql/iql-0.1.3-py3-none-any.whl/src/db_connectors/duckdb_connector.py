import duckdb
import logging
from typing import Dict, List
from pandas import DataFrame
from iqmoql import DatabaseConnector

logger = logging.getLogger(__name__)

class DuckDbConnector(DatabaseConnector):

    def execute_query(self, query: str, completed_dfs: Dict[str, DataFrame]
    ) -> List[DataFrame]:
        
        con = duckdb.connect(database=":memory:")
        
        try:
            # Register each of the dataframes to duckdb, so duckdb can query them
            # Other database might require a "load" or "from_pandas()" step to load these
            # to temporary tables. 
            for key, df in completed_dfs.items():
                if df is None:
                    raise ValueError(f"None dataframe for {key}")
                con.register(key, df)

            df = con.query(query).to_df()
            return [df, *completed_dfs.values()]
        except Exception as e:
            logger.exception(f"Error executing SQL DFs: {query}")
            raise e
        finally:
            con.close()