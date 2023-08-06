import requests
import logging
from dataclasses import dataclass
from pandas import DataFrame
from iqmoql import IqmoQlExtension, register_extension, SubQuery
from typing import Dict, List, Optional

logger=logging.getLogger(__name__)


@dataclass
class RestSubQuery(SubQuery):
    input_parameters = Dict[str, str]

@dataclass
class RestExtension(IqmoQlExtension):
    """Keyword: the function name used in the SQL, such as query_somesite(...)
    base_url: The constant part of the URL path, such as https://www.somesite.com/abc/api
    path: The variable part of the URL path, which will be passed in the function as: query_somesite(path='/data/something', 

    """
    
    keyword: str
    base_url: str
    path: Optional[str]

    constant_params: Dict[str, str] 

    # Params that will always be passed, such as: 
    # api_key: somekey
    # or file_type: json 

    def execute(self, sq: RestSubQuery) -> DataFrame:
        if sq.populate_from_cache() and sq.dataframe is not None:
            return sq.dataframe

        query_string = self.strip_keyword_wrapper(sq.subquery)

        if FRED_API_KEY is None:
            raise ValueError("FRED_API_KEY not set, cannot run")
        else:
            if "api_key" in query_string:
                raise ValueError("api_key is hardcoded in the query")
            elif "file_type" in query_string and "file_type=json" not in query_string:
                raise ValueError("file_type is set, and not to JSON")
            else:
                if "?" not in query_string:
                    query_string += "?"
                query_string += f"&api_key={FRED_API_KEY}"
                if "file_type=json" not in query_string:
                    query_string+="&file_type=json"

                logger.info(f"Querying: {query_string}")
                resp = requests.get(query_string)
                if resp.status_code!=200:
                    raise ValueError(f"Received status {resp.status_code}, cannot process. Result: {resp.text}")
                
                json = resp.json()

                firstlist = next((value for value in json.values() if isinstance(value, list)), None)

                if firstlist is None:
                    dataframe = DataFrame(json)
                else:
                    dataframe = DataFrame(firstlist)

                sq.dataframe=dataframe
                sq.save_to_cache()
                return dataframe
            
def register_extension_rest(keyword, url: str, path: Optional[str], constant_params: Dict[str, str]):
    extension = RestExtension(keyword, url, constant_params)

    register_extension(extension)