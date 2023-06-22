from pydantic import BaseModel
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

class Response(BaseModel):
    skills: List[str]
    
    
class RequestPDF(BaseModel):
    """
    DataModel for Request PDF
    """
    pdf : bytes 

class AddDBRequest(BaseModel):
    resume_name : str 

class UpdateDBRequest(BaseModel):
    resume_text : str 
    skills : Optional[List]
    
class ResponseJDResume(BaseModel):
    skills: List[str]
    required_skills : List[str]
    Percentage : Optional[float] 
