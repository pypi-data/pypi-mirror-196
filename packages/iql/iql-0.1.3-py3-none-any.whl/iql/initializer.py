import configparser
import os
import logging
from iql import iqmoql as ql
import pathlib

logger = logging.getLogger(__name__)

def initialize():
    """Initializes the extensions and database"""

    configfile = f"{os.path.dirname(__file__)}/config.ini"
    keyfile = f"{os.path.dirname(__file__)}/keys.ini"

    if not pathlib.Path(configfile).exists():
        raise ValueError(f"{configfile} does not exist")
    
    if not pathlib.Path(keyfile).exists():
        logger.info(f"{keyfile} doesn't exist")

    config = configparser.ConfigParser()
    config.read(configfile)
    
    keys = configparser.ConfigParser()
    keys.read(keyfile)
    
    # Sets the prefix for each dataframe name
    DFPREFIX = config.get("settings", "DB_MODULE", fallback="df")
    ql._DFPREFIX = DFPREFIX

    # Default database module
    dbmodule_name = config.get("settings", "DB_MODULE", fallback="duckdb")
    if dbmodule_name is None:
        raise ValueError("DB_MODULE not set in config")
    elif dbmodule_name == "duckdb":
        from iql.db_connectors import duckdb_connector as ddc
        db_con = ddc.DuckDbConnector()
        ql._DBCONNECTOR = db_con

    # Caching Settings
    ql.USE_FILE_CACHE = config.get("settings", "USE_FILE_CACHE", fallback=None)
    ql.CACHE_PERIOD = config.get("settings", "CACHE_PERIOD", fallback=None)

    # Enable AWS S3 
    if config.get("settings", "AWS_S3_ENABLE", fallback=False):
        from iql.extensions import aws_s3_extension as ase
        ase.register_extension_aws_s3()

    # Enable BBG BQL
    if config.get("settings", "BBG_ENABLE", fallback=False):
        try:
            from iql.bbg_bql import bql_extension as be

            max_concurrent = config.get("bql", "max_concurrent", fallback=128)
            from iql.bbg_bql import bql_wrapper as bw
            bw._MAX_CONCURRENT = max_concurrent

            be.register_extension_bql()
        except Exception:
            logger.exception("Unable to initialize BQL, make sure you're running inside Bloomberg BQuant")

    # Enable FRED. Requires a FRED_API_KEY in keys.ini.
    if config.get("settings", "FRED_ENABLE", fallback=False):
        fred_key = keys.get("keys", "FRED_API_KEY", fallback=None) # type: ignore
        
        if fred_key is None:
            logger.warning("FRED_API_KEY not set in keys.ini, cannot enable FRED extension")
        else:
            from iql.extensions import fred_extension as fe
            fe.FRED_API_KEY = fred_key
            fe.register_extension_fred()


    # Enable KAGGLE. Requires a KAGGLE_USERNAME and KAGGLE_KEY in keys.ini.
    if config.get("settings", "KAGGLE_ENABLE", fallback=False):
        kaggle_username = keys.get("keys", "KAGGLE_USERNAME", fallback=None)
        kaggle_key = keys.get("keys", "KAGGLE_KEY", fallback=None)

        if kaggle_username is None or kaggle_key is None:
            logger.warning("KAGGLE_USERNAME or KAGGLE_KEY is not set in keys.ini, cannot enable Kaggle extension")
        else:
            os.environ["KAGGLE_KEY"] = kaggle_key
            os.environ["KAGGLE_USERNAME"] = kaggle_username
            
            from iql.extensions import kaggle_extension as ke
            ke.register_extension_kaggle()
