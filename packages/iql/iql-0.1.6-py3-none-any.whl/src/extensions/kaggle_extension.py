import os
import requests
import logging
import pandas as pd

from typing import List
from dataclasses import dataclass
from pandas import DataFrame
from iqmoql import IqmoQlExtension, register_extension, SubQuery

import kaggle

logger=logging.getLogger(__name__)

EXTENSION_KEYWORD = "query_kaggle"

_KAGGLE_API = None
_KAGGLE_DOWNLOAD_DIR = None


def get_api():
    global _KAGGLE_API 
    if _KAGGLE_API is None:
        api = kaggle.KaggleApi()
        api.authenticate()
        _KAGGLE_API = api
    
    return _KAGGLE_API

@dataclass
class KaggleExtension(IqmoQlExtension):
    keyword: str = EXTENSION_KEYWORD

    def executeimpl(self, options: str) -> DataFrame:
        api = get_api() # type :ignore
        global _KAGGLE_API
        query_array = options.split("/")

        if len(query_array) != 3:
            raise ValueError("Format is: query_kaggle('username/datasetname/filename')")
        
        dataset = f"{query_array[0]}/{query_array[1]}"
        filename = query_array[2]

        (f"Retrieving {dataset} file {filename}")
        success = api.dataset_download_file(dataset=dataset, file_name=filename)

        if _KAGGLE_DOWNLOAD_DIR is not None:
            filepath = os.path.join(_KAGGLE_DOWNLOAD_DIR, filename)
        else:
            filepath = filename

        if os.path.isfile(filepath + ".zip"):
            filepath = filepath + ".zip"
        if not os.path.isfile(filepath):
            raise ValueError(f"Unable to download: {options} {filepath}")

        # Could always bypass read_csv here and use DuckDB's CSV directly
        # Would have to modify upstream code, and substitute: 
        # select * from 'filename.csv'
        # Did some perf testing and didn't see a significant difference

        if filename.lower().endswith(".xlsx"):
            dataframe = pd.read_excel(filepath)
        elif filename.lower().endswith(".csv"):
            dataframe = pd.read_csv(filepath)
        else:
            raise ValueError("Unknown file extension. Only XLSX and CSV are supported right now.")
        renames = {}
        for col in dataframe.columns:
            newcol = col.replace("(", "_").replace(")", "_").replace("#", "")
            if newcol!=col:
                renames[col] = newcol

        if len(renames) > 0:
            dataframe=dataframe.rename(columns=renames)

        return dataframe
        
def register_extension_kaggle():
    extension = KaggleExtension()
    register_extension(extension)

def find_datasets(search_string: str):
    api = get_api()
    datasets = api.dataset_list(search=search_string)
    for l in datasets:
        (f"{l.ref} : {l.title} {l.size}, id={l.id}") # type: ignore
    
    return datasets

def list_dataset_files(dataset_name: str) -> List[str]:
    """ Example: "yakinrubaiat/bangladesh-weather-dataset"""
    r = get_api().dataset_list_files(dataset_name)

    files: List[str] = [f"{dataset_name}/{f.name}" for f in r.files] # type: ignore
    
    return files


