from fastapi import APIRouter, FastAPI, UploadFile, File
import pdfplumber 
import io 
router = APIRouter()

from src.data_models import *

from src.pipeline import pipe_line,skill_extractor, pipe_line_for_resume_jd_match


@router.post("/extract_skills/", 
            tags=["Skills Extraction"],
            summary= "Extract Skills from Resume",
            response_model=Response,
            response_model_exclude_none=True)
async def update_item(train_args: Request):

    pdf_path = train_args.pdf
    skills = skill_extractor(pdf_path)

    return skills

@router.post("/extract_skills_from_uploaded_resume/", 
            tags=["Skills Extraction from uploaded Resume"],
            summary= "Extract Skills from Resume uploaded",
            response_model=Response,
            response_model_exclude_none=True)
async def update_item_from_pdf(file: UploadFile = File(...)):
    file_content = await file.read()
    file_object = io.BytesIO(file_content)
    skills = pipe_line(file.filename,file_object)

    return skills

@router.post("/matching_resume_with_job_description/", 
            tags=["Matching Resume with Job Description"],
            summary= "Provide Match Percentage for Resume with Job Description",
            response_model=ResponseJDResume,
            response_model_exclude_none=True)
async def update_item_matching(file_resume: UploadFile = File(...),file_jd:UploadFile = File(...)):
    file_resume_content = await file_resume.read()
    file_resume_object = io.BytesIO(file_resume_content)
    file_jd_content = await file_jd.read()
    file_jd_object = io.BytesIO(file_jd_content)
    skills = pipe_line_for_resume_jd_match(file_resume.filename,file_resume_object,file_jd.filename,file_jd_object)

    return skills