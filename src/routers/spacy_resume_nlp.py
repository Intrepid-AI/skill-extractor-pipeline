import io 

from src.logger import get_logger

from fastapi import APIRouter, UploadFile, File

from src.data_models import *

from src.services.spacy_resume_nlp.pipeline import pipeline_skills_extraction,skill_extractor, pipeline_for_resume_jd_match

LOGGER = get_logger(__name__)

router = APIRouter()

@router.post("/extract_skills/", 
            tags=["skills_extract"],
            summary= "Extract Skills from Resume",
            response_model=Response,
            response_model_exclude_none=True)
async def update_item(train_args: RequestSkills):
    
    LOGGER.info("Request received for skills_extract : {0}".format(train_args))
    pdf_path = train_args.pdf
    skills = skill_extractor(pdf_path)
    LOGGER.info("Response sent for skills_extract : {0}".format(skills))
    
    return skills

@router.post("/extract_skills_from_uploaded_resume/", 
            tags=["skills_extract"],
            summary= "Extract Skills from Resume uploaded",
            response_model=Response,
            response_model_exclude_none=True)
async def update_item_from_pdf(file: UploadFile = File(...)):

    file_content = await file.read()
    file_object = io.BytesIO(file_content)
    skills = pipeline_skills_extraction(file.filename,file_object)

    return skills

@router.post("/matching_resume_with_job_description/", 
            tags=["similarity_matching"],
            summary= "Provide Match Percentage for Resume with Job Description",
            response_model=ResponseJDResume,
            response_model_exclude_none=True)
async def update_item_matching(file_resume: UploadFile = File(...),file_jd:UploadFile = File(...)):

    file_resume_content = await file_resume.read()
    file_resume_object = io.BytesIO(file_resume_content)
    file_jd_content = await file_jd.read()
    file_jd_object = io.BytesIO(file_jd_content)
    skills = pipeline_for_resume_jd_match(file_resume.filename,file_resume_object,file_jd.filename,file_jd_object)

    return skills