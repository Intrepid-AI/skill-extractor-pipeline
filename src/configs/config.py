import os
from pydantic import BaseSettings

class Settings(BaseSettings):

    version: str = "V-1"
    app_name: str = "Skills_Exctractor"
    logs_folder: str = "logs"
    #models_folder: str = "models"
    
settings = Settings()