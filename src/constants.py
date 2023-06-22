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

    # Received File Paths
    RECEIVED_DATA = "data"
    RESUME_PATH = "resume"

    RESUME_AND_JD = "resume_and_jd"

    JD = "job_description"

    MONGO_DB = "ivdb"
    MONGO_COLLECTIONS = {"task_status":"task_status", 
                        "resume_dump":"resume_dump",
                         "jd_dump":"jd_dump",
                         "task_info":"task_info"}
    
    TASK_STATUS = {"progress":"in_progress",
                   "completed":"completed",
                    "failed":"failed"
                }
    
    ALLOWED_FILE_TYPES = {"pdf":"application/pdf",
                                  "doc":"application/msword",
                                  "docx":"application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                }
    
