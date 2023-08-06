# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

import logging
from dataclasses import dataclass
from pandas import DataFrame
from typing import Tuple, Optional, Dict
from iql.iqmoql import IqmoQlExtension, register_extension, SubQuery
import boto3
import re
import os
from pathlib import Path
from iql import q_cache

logger = logging.getLogger(__name__)

_PATTERN = re.compile(r"s3://(.*?)/(.*)")

BOTO3_S3_RESOURCES: Dict[str, object] = {}
BOTO3_S3_RESOURCE_DEFAULT = None

def get_boto3_resource_for_request(url: str) -> object:
    """boto3 resources may be pre-created and saved in
    aws_s3_extension.BOTO3_S3_RESOURCES.
    Or, override this for your custom implementation."""
    for prefix, boto3obj in BOTO3_S3_RESOURCES:
        if url.startswith(prefix):
            return boto3obj
    else:
        # Return the default
        return boto3.resource("s3")


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
        if self.temp_file_directory is None:
            local_path = filename
        else:
            local_path = os.path.join(self.temp_file_directory, filename)

        return (bucket, key, local_path)

    def execute(self, sq: SubQuery) -> Optional[DataFrame]:

        url = sq.get_query()
        bucket, key, local_path = self.options_to_tuple(url)

        # For path replacement cases, the q_cache just stores a reference to the path.
        # when the file is expired, q_cache returns None
        obj = q_cache.get(local_path)
        expired = obj is None  # if obj is None, then the file is expired

        if Path(local_path).exists() and not expired and self.allow_cache_read(sq):
            logger.info(f"{local_path} exists, not downloading again")
            return None
        else:
            logger.info(f"Downloading {key} to {local_path}")

            s3_resource = get_boto3_resource_for_request(url)

            s3_resource.Bucket(bucket).download_file(key, local_path)  # type: ignore

            # Just save the path name as the object
            q_cache.save(
                local_path,
                local_path,
                self.get_cache_period(),
                self.use_file_cache(),
                type="awss3",
            )
            return None


def register(keyword: str):
    extension = AwsS3Extension(keyword=keyword)
    register_extension(extension)
