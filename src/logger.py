import logging, logging.handlers
import yaml
from pathlib import Path
import sys
import os

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # project root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH

from src.constants import Constants

with open(ROOT / Constants.CONFIG_APP.value) as reader:
    file_loc = yaml.load(reader, Loader=yaml.FullLoader)["log"]

logging.basicConfig(format="%(asctime)s -- %(levelname)s -- %(name)s -- %(message)s")

def get_logger(name):
    log_level = Constants.LOG_LEVEL.value
    LOGGER = logging.getLogger(name)

    if log_level == "DEBUG":
        LOGGER.setLevel(logging.DEBUG)
    elif log_level == "INFO":
        LOGGER.setLevel(logging.INFO)
    elif log_level == "ERROR":
        LOGGER.setLevel(logging.ERROR)
    else:
        LOGGER.setLevel(logging.INFO)

    handler_file = logging.handlers.RotatingFileHandler(
        file_loc,
        mode="a",
        maxBytes=10 * 1024 * 1024,
        backupCount=50,
        encoding=None,
        delay=0,
    )

    log_formatter = logging.Formatter(
        "%(asctime)s -- %(levelname)s -- %(name)s -- %(funcName)s -- (%(lineno)d) -- %(message)s"
    )

    handler_file.setFormatter(log_formatter)

    if log_level == "DEBUG":
        handler_file.setLevel(logging.DEBUG)
    elif log_level == "INFO":
        handler_file.setLevel(logging.INFO)
    elif log_level == "ERROR":
        handler_file.setLevel(logging.ERROR)
    else:
        handler_file.setLevel(logging.INFO)

    LOGGER.addHandler(handler_file)
    return LOGGER
