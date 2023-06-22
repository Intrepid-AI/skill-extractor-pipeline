from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict 

'''
Todo :
    1. Format it as standard json response
'''
class RequestSkills(BaseModel):
    """
    DataModel for Request
    """
    pdf : str 
    
class RequestPDF(BaseModel):
    """
    DataModel for Request PDF
    """
    pdf : bytes

class ResponseBase(BaseModel):
    '''
    Base response model for all responses from API
    '''
    ID: str
    task_name: str
    status: str
    timestamp : datetime
    code: int
    error: Optional[str] = None
    
class ResponseSkills(ResponseBase):
    '''
    Response model for resume skills
    '''
    timetaken : Optional[str] = None
    skills: Optional[List[str]] = None

class ResponseJDResume(ResponseBase):
    '''
    Response model for resume jd matching
    '''
    timetaken : Optional[str] = None
    skills_res : Optional[List] = None
    skills_jd : Optional[List] = None
    similiarity : Optional[float] = None
