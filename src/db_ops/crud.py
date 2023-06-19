from src.data_models import AddDBRequest,UpdateDBRequest
from bson import ObjectId

'''
Todo:
    1. Dont take collection as a input arg, its anyway fixed
    2. Create different collection for status, pdf files content, pdf file entities extracted
'''
def add_db_request(collection,resume_name : str):

    record = {"resume_name":resume_name}
    db_item = collection.insert_one(record)

    return str(db_item.inserted_id)


def update_db(collection,u_id: str,resume_text:str,skills:None):

    update= {"resume_text":resume_text,"skills":skills}
    filter = {"_id":ObjectId(u_id)}
    updated = {"$set":update}
    result = collection.update_one(filter, updated)
     
def add_db_request_jd_resume(collection,resume_name : str,jd_name:str):
    record = {"resume_name":resume_name,"job_description_name":jd_name}
    db_item = collection.insert_one(record)

    return str(db_item.inserted_id)

def update_db_jd_resume(collection,u_id: str,resume_text:str, jd_text:str,match:None, skills:None,skills_jd:None):

    update= {"resume_text":resume_text,"job_description_text":jd_text, "skills_in_resume":skills,"skills_required":skills_jd,"matching_percentage":match}
    filter = {"_id":ObjectId(u_id)}
    updated = {"$set":update}
    result = collection.update_one(filter, updated)