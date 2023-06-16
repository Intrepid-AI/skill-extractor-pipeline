from pydantic import BaseModel
from typing import Optional, List, Dict 

class RequestSkills(BaseModel):
    """
    DataModel for Request
    """
    pdf : str 

class Response(BaseModel):
    SKILLS: List[str]
    
    
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
    SKILLS: List[str]
    required_skills : List[str]
    Percentage : Optional[float] 
