from src.data_models import AddDBRequest,UpdateDBRequest
from bson import ObjectId

def add_db_request(collection,resume_name : str):
    record = {"resume_name":resume_name}
    db_item = collection.insert_one(record)

    return str(db_item.inserted_id)


def update_db(collection,u_id: str,resume_text:str,skills:None):

    update= {"resume_text":resume_text,"skills":skills}
    filter = {"_id":ObjectId(u_id)}
    updated = {"$set":update}
    result = collection.update_one(filter, updated)
     