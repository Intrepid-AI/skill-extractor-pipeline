from datetime import datetime

from pydantic import BaseModel

from typing import Optional, List

class BaseInfo(BaseModel):
    task_name : str 
    status : str 
    timestamp : datetime
    timetaken : str

class Extraction(BaseInfo):
    extracted_text : Optional[str] = None
    skills : Optional[List] = None

class Matching(BaseInfo):
    resume_text : Optional[str] = None
    jd_text : Optional[str] = None
    skills_res : Optional[List] = None
    skills_jd : Optional[List] = None
    similiarity : Optional[float] = None