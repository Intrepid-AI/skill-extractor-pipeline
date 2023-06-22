import pymongo
from pymongo import MongoClient
from pathlib import Path
from yaml.loader import SafeLoader
import yaml
import sys

FILE = Path(__file__).resolve()
ROOT = FILE.parents[2]  # project root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
    
from src.constants import Constants
from src.logger import get_logger

LOGGER = get_logger(__name__)

with open(Constants.CONFIG_APP.value) as f:
    app_config = yaml.load(f, Loader=SafeLoader)

def get_mongo_client():
    """
    Returns the mongo client object for the database initializing 
    all the collections from constants
    """
    DB_HOST = app_config.get("db_host")
    DB_PORT = app_config.get("db_port")

    MONGO_DB_URL = "mongodb://{}:{}".format(DB_HOST, DB_PORT)

    try:
        client = MongoClient(MONGO_DB_URL)
        LOGGER.debug('Mongo client initialized')

        # initialize all mongo collections from constants
        for _,coll in Constants.MONGO_COLLECTIONS.value.items():
            client[Constants.MONGO_DB.value][coll]
            LOGGER.debug("Collection initialized : {0}".format(coll))

        LOGGER.info('Mongo client & collections initialized successfully')
        
        return client
    
    except Exception as e:
        
        LOGGER.error('exception occured in get_mongo_client() - {0}'.format(e))


if __name__=='__main__':

    get_mongo_client()