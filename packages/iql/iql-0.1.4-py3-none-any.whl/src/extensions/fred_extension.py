import requests
import logging
from dataclasses import dataclass
from pandas import DataFrame
from iqmoql import IqmoQlExtension, register_extension, SubQuery

logger=logging.getLogger(__name__)

EXTENSION_KEYWORD = "query_fred"

FRED_API_KEY = None

@dataclass
class FredExtension(IqmoQlExtension):
    keyword: str = EXTENSION_KEYWORD

    def executeimpl(self, options: str) -> DataFrame:
        query_string = options
        
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
                
                return dataframe
            
            
def register_extension_fred():
    extension = FredExtension()
    register_extension(extension)