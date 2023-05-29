import pymongo
from pymongo import MongoClient
from pathlib import Path
from yaml.loader import SafeLoader
import yaml
import sys


FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # project root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
    
from src.constants import Constants
from src.logger import get_logger

with open(Constants.CONFIG_APP.value) as f:
    app_config = yaml.load(f, Loader=SafeLoader)


DB_HOST = app_config.get("db_host")
DB_PORT = app_config.get("db_port")
DB_NAME = app_config.get("db_name")

MONGO_DB_URL = "mongodb://{}:{}".format(DB_HOST, DB_PORT)


client = MongoClient(MONGO_DB_URL)

database = client[DB_NAME]
collection = database[DB_NAME]