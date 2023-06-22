from bson import ObjectId

from src.constants import Constants

from src.data_models import AddDBRequest,UpdateDBRequest


'''
Todo:
    1. Create proper data models for db insertions whenever happens
'''

def status_update(client, status : str):

    collection = client[Constants.MONGO_COLLECTIONS.value["task_status"]]

    record = {"status":status}

    db_item = collection.insert_one(record)

    return str(db_item.inserted_id)

def add_task_info(client, u_id: str, resume_text:str, skills:None):

    collection = client[Constants.MONGO_COLLECTIONS.value["task_info"]]

    update= {"resume_text":resume_text,"skills":skills}

    filter = {"_id":ObjectId(u_id)}

    updated = {"$set":update}

    result = collection.update_one(filter, updated)
    
    return

def update_db_jd_resume(client, u_id: str, resume_text:str, jd_text:str, match:None, skills_res:None, skills_jd:None):
    '''
    Todo :
        1. Combine this in add_task_info after datamodels based argument is enabled IF POSSIBLE
    '''
    collection = client[Constants.MONGO_COLLECTIONS.value["task_info"]]

    update= {"resume_text":resume_text, "job_description_text":jd_text, "skills_in_resume":skills_res, "skills_required":skills_jd, "matching_percentage":match}
    
    filter = {"_id":ObjectId(u_id)}
    
    updated = {"$set":update}
    
    result = collection.update_one(filter, updated)