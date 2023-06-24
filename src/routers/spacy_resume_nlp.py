import io 
import os
import time
import copy
from functools import partial

from src.logger import get_logger

from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException

from src.data_models import *

from src.constants import Constants

from src.services.spacy_resume_nlp.pipeline import (
    pipeline_skills_extraction, pipeline_for_resume_jd_match)

from src.db_ops import (get_mongo_client, status_update, task_update_extraction,
                        task_update_matching, Extraction, Matching)

from src.utilities import Directory_Structure, save_file, Send_Response

from src.api_ops import ResponseCodes

### Code Initialization

dir_manager = Directory_Structure()

LOGGER = get_logger(__name__)

router = APIRouter()

###                       

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

'''
Todo:
    1. Create skills extract from text only
'''

response_manager = Send_Response(LOGGER, status_update)

@router.get("/health", tags=["health_check"])
async def checkhealth():
    return {"status":200}

@router.post("/extract_skills_upload/", 
            tags=["skills_extract"],
            summary= "Extract Skills from file uploaded",
            response_model=ResponseSkills,
            response_model_exclude_none=True)
async def skill_extraction_from_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):

    ts_start = time.time()

    u_id = status_update(client, coll_name=Constants.MONGO_COLLECTIONS.value["coll_extraction"],
                         status=Constants.TASK_STATUS.value["progress"])

    response_base = ResponseBase(**{"ID": u_id,
                    "task_name": "spacy_skills_extract",
                    "timestamp": datetime.now().strftime('%F %T.%f')[:-2],
                    "status": Constants.TASK_STATUS.value["progress"],
                    "code": 200})
        
    LOGGER.info("Request received for extract_skills : {0}".format(file.filename))
    
    file_dir = dir_manager()
    
    up_filename = file.filename
    
    # Save the file to disk
    save_file_name = os.path.join(file_dir,os.path.splitext(up_filename)[-2] + \
                                "_"+u_id + os.path.splitext(up_filename)[-1])

    file_type = file.content_type

    # Verify if the file type is supported
    if file_type not in list(Constants.ALLOWED_FILE_TYPES.value.values()):

        LOGGER.error("File type not supported for extract_skills : {0}".format(file_type))

        response_base = response_manager.update_response(db_client=client, 
                                         resp_object=response_base, 
                                         status=Constants.TASK_STATUS.value["failed"],
                                         code=ResponseCodes.ERRORS_415.value["code"],
                                         error=ResponseCodes.ERRORS_415.value["415_filetype"])

        raise HTTPException(status_code=response_base.code, detail=response_base.error)

    file_content = await file.read()
    file_object = io.BytesIO(file_content)

    # Create a copy of the file object to be used for saving the file to disk
    fobj = copy.copy(file_object)
    background_tasks.add_task(save_file, fobj, save_file_name)

    # Call the pipeline for skills extraction
    try:
        result_dict = pipeline_skills_extraction(file_object, file_type, save_file_name)
    except Exception as e:
        LOGGER.error("Exception occured in pipeline_skills_extraction : {0}".format(e))

        response_base = response_manager.update_response(db_client=client, 
                                         resp_object=response_base, 
                                         status=Constants.TASK_STATUS.value["failed"],
                                         code=ResponseCodes.ERRORS_500.value["code"],
                                         error=ResponseCodes.ERRORS_500.value["500_IntServer"])

        raise HTTPException(status_code=response_base.code, detail=response_base.error)

    response_base = response_manager.update_response(db_client=client, 
                                        resp_object=response_base, 
                                        status=Constants.TASK_STATUS.value["completed"])
    
    time_taken = time.time() - ts_start

    # Create a dictionary to be inserted into the database
    db_dict_extract = Extraction(**response_base.dict(), **result_dict, **{"timetaken": time_taken})  

    task_update_extraction(client=client, ID=u_id, db_dict=db_dict_extract)

    # Create a dictionary to be sent as response
    response_skills = ResponseSkills(**response_base.dict(), **result_dict, **{"timetaken": time_taken})

    LOGGER.info("Response sent for skills_extract : {0}".format(response_skills.dict()))

    return response_skills

@router.post("/match_resume_with_jd/",
            tags=["similarity_matching"],
            summary= "Provide Match Percentage for Resume with Job Description",
            response_model=ResponseJDResume,
            response_model_exclude_none=True)
async def skill_matching(file_resume: UploadFile = File(...), 
                               file_jd:UploadFile = File(...),
                                background_tasks: BackgroundTasks = BackgroundTasks()):

    ts_start = time.time()

    u_id = status_update(client, coll_name=Constants.MONGO_COLLECTIONS.value["coll_matching"],
                         status=Constants.TASK_STATUS.value["progress"])

    response_base = ResponseBase(**{"ID": u_id,
                    "task_name": "spacy_similarity_matching",
                    "timestamp": datetime.now().strftime('%F %T.%f')[:-2],
                    "status": Constants.TASK_STATUS.value["progress"],
                    "code": 200})

    LOGGER.info("Request received for matching_resume_with_job_description : {0}, {1}".format(file_resume.filename, file_jd.filename))

    file_dir = dir_manager()
    
    up_filename_res, up_filename_jd = file_resume.filename, file_jd.filename
    
    # Saving the files in the directory
    save_file_name_res = os.path.join(file_dir,os.path.splitext(up_filename_res)[-2] + \
                                "_"+u_id + os.path.splitext(up_filename_res)[-1])

    save_file_name_jd = os.path.join(file_dir,os.path.splitext(up_filename_jd)[-2] + \
                                "_"+u_id + os.path.splitext(up_filename_jd)[-1])

    # Verifying the file types
    file_type_res, file_type_jd = file_resume.content_type, file_jd.content_type

    if file_type_res not in list(Constants.ALLOWED_FILE_TYPES.value.values()) or \
        file_type_jd not in list(Constants.ALLOWED_FILE_TYPES.value.values()):

        LOGGER.error("File type not supported for matching_resume_with_\
                     job_description : {0}, {1}".format(file_type_res, file_type_jd))

        response_base = response_manager.update_response(db_client=client, 
                                         resp_object=response_base, 
                                         status=Constants.TASK_STATUS.value["failed"],
                                         code=ResponseCodes.ERRORS_415.value["code"],
                                         error=ResponseCodes.ERRORS_415.value["415_filetype"])

        raise HTTPException(status_code=response_base.code, detail=response_base.error)

    file_resume_content = await file_resume.read()
    file_object_res = io.BytesIO(file_resume_content)

    # Create a copy of the file object to be used for saving the file to disk
    fobj_res = copy.copy(file_object_res)
    background_tasks.add_task(save_file, fobj_res, save_file_name_res) # Save the file to disk in background

    file_jd_content = await file_jd.read()
    file_object_jd = io.BytesIO(file_jd_content)

    # Create a copy of the file object to be used for saving the file to disk
    fobj_jd = copy.copy(file_object_jd)
    background_tasks.add_task(save_file, fobj_jd, save_file_name_jd) # Save the file to disk in background

    # Call the pipeline for resume jd matching
    try:
        result_dict = pipeline_for_resume_jd_match(file_object_res=file_object_res, file_type_res=file_type_res,
                                                   save_file_name_res=save_file_name_res,
                                                   file_object_jd=file_object_jd, file_type_jd=file_type_jd,
                                                   save_file_name_jd=save_file_name_jd)

    except Exception as e:
        LOGGER.error("Exception occured in pipeline_for_resume_jd_match : {0}".format(e))

        response_base = response_manager.update_response(db_client=client, 
                                         resp_object=response_base, 
                                         status=Constants.TASK_STATUS.value["failed"],
                                         code=ResponseCodes.ERRORS_500.value["code"],
                                         error=ResponseCodes.ERRORS_500.value["500_IntServer"])

        raise HTTPException(status_code=response_base.code, detail=response_base.error)

    response_base = response_manager.update_response(db_client=client, 
                                        resp_object=response_base, 
                                        status=Constants.TASK_STATUS.value["completed"])
    
    time_taken = time.time() - ts_start
    
    # Create a dictionary to be inserted into the database
    db_dict_match = Matching(**response_base.dict(), **result_dict, **{"timetaken": time_taken})

    task_update_matching(client=client, ID=u_id, db_dict=db_dict_match)

    # Create a dictionary to be sent as response
    response_jdres = ResponseJDResume(**response_base.dict(), **result_dict, **{"timetaken": time_taken})
    
    LOGGER.info("Response sent for matching_resume_with_job_description : {0}".format(response_jdres.dict()))
    
    return response_jdres


