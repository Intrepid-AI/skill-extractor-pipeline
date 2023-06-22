import io 
import os

from src.logger import get_logger

from fastapi import APIRouter, UploadFile, File, BackgroundTasks

from src.data_models import *

from src.constants import Constants

from src.services.spacy_resume_nlp.pipeline import (
    pipeline_skills_extraction, pipeline_for_resume_jd_match)

from src.db_ops import get_mongo_client, status_update

from src.utilities import Directory_Structure, save_file

dir_manager = Directory_Structure()

LOGGER = get_logger(__name__)

router = APIRouter()

# MongoDB client and database
client = None
database = None

@router.on_event("startup")
async def startup_event():
    global client, database
    # Initialize MongoDB client
    client = get_mongo_client()

@router.on_event("shutdown")
async def shutdown_event():
    # Close the MongoDB client connection
    if client is not None:
        client.close()

@router.post("/extract_skills_from_uploaded_resume/", 
            tags=["skills_extract"],
            summary= "Extract Skills from Resume uploaded",
            response_model=Response,
            response_model_exclude_none=True)
async def update_item_from_pdf(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):

    LOGGER.info("Request received for skills_extract : {0}".format(file.filename))
    
    file_dir = dir_manager()
    up_filename = file.filename
    u_id = status_update(client=client, status=Constants.TASK_STATUS.value["progress"])
    save_file_name = os.path.join(file_dir,os.path.splitext(up_filename)[-2] + \
                                u_id + os.path.splitext(up_filename)[-1])
    background_tasks.add_task(save_file, file, save_file_name)

    file_type = file.content_type

    if file_type not in list(Constants.ALLOWED_FILE_TYPES.value.values()):
        '''
        Todo:
        1. Create a proper error response code for unknown file type
        '''
        return -1

    try:
        skills = pipeline_skills_extraction(file, file_type, save_file_name, u_id)
    except Exception as e:
        LOGGER.error("Exception occured in pipeline_skills_extraction : {0}".format(e))
        status_update(client=client, status=Constants.TASK_STATUS.value["failed"],u_id=u_id)

    status_update(client=client, status=Constants.TASK_STATUS.value["completed"])
    
    LOGGER.info("Response sent for skills_extract : {0}".format(skills))

    return skills

@router.post("/matching_resume_with_job_description/",
            tags=["similarity_matching"],
            summary= "Provide Match Percentage for Resume with Job Description",
            response_model=ResponseJDResume,
            response_model_exclude_none=True)
async def update_item_matching(file_resume: UploadFile = File(...), 
                               file_jd:UploadFile = File(...),
                                background_tasks: BackgroundTasks = BackgroundTasks()):

    LOGGER.info("Request received for matching_resume_with_job_description : {0}, {1}".format(file_resume.filename, file_jd.filename))

    file_dir = dir_manager()
    up_filename_res, up_filename_jd = file_resume.filename, file_jd.filename
    u_id = status_update(client=client, status=Constants.TASK_STATUS.value["progress"])

    save_file_name_res = os.path.join(file_dir,os.path.splitext(up_filename_res)[-2] + \
                                u_id + os.path.splitext(up_filename_res)[-1])
    background_tasks.add_task(save_file, file_resume, save_file_name_res)

    save_file_name_jd = os.path.join(file_dir,os.path.splitext(up_filename_jd)[-2] + \
                                u_id + os.path.splitext(up_filename_jd)[-1])
    background_tasks.add_task(save_file, file_jd, save_file_name_jd)

    file_type_res, file_type_jd = file_resume.content_type, file_jd.content_type

    if file_type_res not in list(Constants.ALLOWED_FILE_TYPES.value.values()) or \
        file_type_jd not in list(Constants.ALLOWED_FILE_TYPES.value.values()):
        '''
        Todo:
        1. Create a proper error response code for unknown file type
        '''
        return -1

    file_resume_content = await file_resume.read()
    file_resume_object = io.BytesIO(file_resume_content)
    file_jd_content = await file_jd.read()
    file_jd_object = io.BytesIO(file_jd_content)
    skills = pipeline_for_resume_jd_match(file_resume.filename,file_resume_object,file_jd.filename,file_jd_object)
    status_update(client=client, status=Constants.TASK_STATUS.value["completed"])
    LOGGER.info("Response sent for matching_resume_with_job_description : {0}".format(skills))
    return skills