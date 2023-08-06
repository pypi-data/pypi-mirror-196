# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

import requests
import logging
from dataclasses import dataclass
from typing import List, Dict
from pandas import DataFrame
from iql.iqmoql import IqmoQlExtension, register_extension, SubQuery
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.preprocessing import PolynomialFeatures
import pmdarima as pm
import importlib

logger = logging.getLogger(__name__)

@dataclass
class SklearnExtension(IqmoQlExtension):
    keyword: str

    def executeimpl(self, sq: SubQuery) -> DataFrame:

        module = sq.options.get("module")
        model = sq.options.get("model")
        data = sq.options.get("data") 
        
        df = sq.dbcon.sql(f"select * from {data}").to_df()  # type: ignore

        module = importlib.import_module(module)


        #models["0"] = (DummyRegressor(strategy="mean"), x_n)
        #models["1"] = (linear_model.LinearRegression(), x_n)
        return None


def register(keyword: str):
    extension = SklearnExtension(keyword=keyword)
    register_extension(extension)
