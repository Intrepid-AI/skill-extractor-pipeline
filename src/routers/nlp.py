from fastapi import APIRouter, FastAPI, UploadFile, File
import pdfplumber 
import io 
router = APIRouter()

from src.data_models import *

from src.pipeline import pipe_line,skill_extractor


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