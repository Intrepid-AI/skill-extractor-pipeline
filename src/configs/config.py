from pydantic import BaseSettings

class Settings(BaseSettings):
    """ App related setting, limited to developer only
    """
    app_name: str = "Skills_Extractor"
    logs_folder: str = "logs"
    
settings = Settings()