from datetime import datetime

from pydantic import BaseModel

from typing import Optional, List

class BaseInfo(BaseModel):
    '''Base model for all data models'''
    task_name : str 
    status : str 
    timestamp : datetime
    timetaken : str

class Extraction(BaseInfo):
    '''Data model for storing extraction of skills'''
    extracted_text : Optional[str] = None
    skills : Optional[List] = None

class Matching(BaseInfo):
    '''Data model for storing matching of skills related data'''
    resume_text : Optional[str] = None
    jd_text : Optional[str] = None
    skills_res : Optional[List] = None
    skills_jd : Optional[List] = None
    similiarity : Optional[float] = None