import logging
from dataclasses import dataclass
from pandas import DataFrame
from typing import Tuple, Optional
from iqmoql import IqmoQlExtension, register_extension
import s3fs
import re
import os
from pathlib import Path

logger=logging.getLogger(__name__)

EXTENSION_KEYWORD = "query_s3obj"

LOCAL_DIR = None
_PATTERN = re.compile(r"s3://(.*?)/(.*)")
REUSE_DOWNLOAD = True

@dataclass
class AwsS3Extension(IqmoQlExtension):
    keyword: str = EXTENSION_KEYWORD

    def options_to_tuple(self, subquery: str) -> Tuple[str, str, str]:
        # returns bucket, key, local filename

        options = self.strip_keyword_wrapper(subquery)

        # parse the url
        m = _PATTERN.match(options)
        if m is None:
            raise ValueError(f"Doesn't match expected S3 URL pattern: s3://bucket/prefix/key")
        
        bucket = m.group(1)
        key = m.group(2)
        
        filename = key if "/" not in key else key[key.index("/"):]

        if LOCAL_DIR is None:
            local_path = filename
        else:
            local_path = os.path.join(LOCAL_DIR, filename) 

        return (bucket, key, local_path)


    def execute(self, options: str) -> Optional[DataFrame]:
        bucket, key, local_path = self.options_to_tuple(options)

        if Path(local_path).exists():
            logger.debug(f"{local_path} exists")
            return None
        else:
            logger.debug(f"Downloading {key} to {local_path}")
            s3_resource = boto3.resource('s3')
            s3_resource.Bucket(bucket).download_file(key, local_path)
            return None

def register_extension_aws_s3():
    extension = AwsS3Extension()
    register_extension(extension)