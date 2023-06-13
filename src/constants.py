import os
from enum import Enum

class Constants(Enum):
    CONFIG = os.path.join("configurations", "config.yaml")
    SKILLS ="SKILL"
    STOPWORDS = "stopwords"
    WORDNET = "wordnet"
    EXTRACT_STRUCTURE = '(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?"'
    LANGUAGE = "english"
    SPACE = " "
    CORPUS = "en_core_web_lg"
    ENTITY_RULER = "entity_ruler"
    ANNOTATIONS = os.path.join("skills_annotations", "jz_skill_patterns.jsonl")
    LOGS_FOLDER = "logs"
    LOG_LEVEL = "DEBUG"

    CONFIG_APP = (
        os.path.join("configurations", "app.prod.yaml")
        if os.getenv("APP_ENV") == "PROD"
        else os.path.join("configurations", "app.dev.yaml")
    )


    DATA = "data"
    PROCESSED_DATA = "processed"
    RESUME = "resume"
    RESUME_AND_JD = "resume_and_jd"
    JD = "job_description"
