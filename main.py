# python libraries
import time
from typing import Optional
import uuid
import os

# Installed libraries
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# custom modules
from src.configs.config import settings

from src.constants import Constants

from src.routers import checks, nlp

def get_app() -> FastAPI:
  try:
      fast_app = FastAPI(title=settings.app_name)
      return fast_app
  except Exception as e:
      print(f'exception occured in get_app() - {e}')

app = get_app()

app.include_router(checks.router)
app.include_router(nlp.router)
