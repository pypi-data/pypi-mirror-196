# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

import logging
from dataclasses import dataclass
from pandas import DataFrame
from typing import Tuple, Optional
from iql.iqmoql import IqmoQlExtension, register_extension, SubQuery
import boto3
import re
import os
from pathlib import Path

logger = logging.getLogger(__name__)

LOCAL_DIR = None
_PATTERN = re.compile(r"s3://(.*?)/(.*)")


@dataclass
class AwsS3Extension(IqmoQlExtension):
    def get_path_replacement(self, subquery: str) -> str:
        bucket, key, local_path = self.options_to_tuple(subquery)
        return local_path

    def use_path_replacement(self) -> bool:
        return True

    def options_to_tuple(self, subquery: str) -> Tuple[str, str, str]:
        # returns bucket, key, local filename

        # parse the url
        m = _PATTERN.match(subquery)
        if m is None:
            raise ValueError(
                f"Doesn't match expected S3 URL pattern: s3://bucket/prefix/key, {subquery}"
            )

        bucket = m.group(1)
        key = m.group(2)

        filename = key if "/" not in key else key[key.index("/") + 1 :]

        filename = filename.replace("/", "_")
        if LOCAL_DIR is None:
            local_path = filename
        else:
            local_path = os.path.join(LOCAL_DIR, filename)

        return (bucket, key, local_path)

    def execute(self, sq: SubQuery) -> Optional[DataFrame]:
        bucket, key, local_path = self.options_to_tuple(sq.get_query())

        if Path(local_path).exists() and self.allow_cache_read(sq):
            logger.info(f"{local_path} exists, not downloading again")
            return None
        else:
            logger.info(f"Downloading {key} to {local_path}")
            s3_resource = boto3.resource("s3")
            s3_resource.Bucket(bucket).download_file(key, local_path)  # type: ignore
            return None


def register(keyword: str):
    extension = AwsS3Extension(keyword=keyword)
    register_extension(extension)
