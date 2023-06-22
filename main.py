import os

# Installed libraries
from fastapi import FastAPI

# custom modules
from src.configs.config import settings

from src.routers import checks, spacy_resume_nlp

from src.logger import get_logger

from src.constants import Constants

from src.utilities import make_directories

make_directories([Constants.LOGS_FOLDER.value])
assert os.path.isdir(Constants.LOGS_FOLDER.value) == True  # Logs folder exists

LOGGER = get_logger(__name__)

def get_app() -> FastAPI:
    """
    Returns the FastAPI app object
    """
    try:
        fast_app = FastAPI(title=settings.app_name)
        return fast_app
    except Exception as e:
        LOGGER.error('exception occured in get_app() - {0}'.format(e))

app = get_app()
LOGGER.debug("App returned successfully")

app.include_router(checks.router)
app.include_router(spacy_resume_nlp.router)
LOGGER.info("App loading complete")