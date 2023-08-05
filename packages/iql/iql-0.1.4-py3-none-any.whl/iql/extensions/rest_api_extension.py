# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

import logging
from dataclasses import dataclass
from pandas import DataFrame
from iql.iqmoql import IqmoQlExtension, register_extension, SubQuery
from typing import Dict, Optional

logger = logging.getLogger(__name__)


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
        raise ValueError("Implement Me")


def register(keyword, url: str, path: Optional[str], constant_params: Dict[str, str]):
    extension = RestExtension(
        keyword=keyword, base_url=url, constant_params=constant_params, path=path
    )

    register_extension(extension)
