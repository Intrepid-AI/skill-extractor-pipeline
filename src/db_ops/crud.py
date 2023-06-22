from bson import ObjectId

from src.constants import Constants

from .schemas import Matching, Extraction

def status_update(client, coll_name : str, status : str):
    """Function to update the status of the task in the database"""
    # import pdb; pdb.set_trace()
    collection = client[Constants.MONGO_DB.value][coll_name]

    record = {"status":status}

    db_item = collection.insert_one(record)

    return str(db_item.inserted_id)

def task_update_extraction(client, ID: str, db_dict : Extraction):

    collection = client[Constants.MONGO_DB.value][Constants.MONGO_COLLECTIONS.value["coll_extraction"]]

    update = db_dict.dict()
    
    filter = {"_id":ObjectId(ID)}
    
    updated = {"$set":update}
    
    result = collection.update_one(filter, updated)

    return

def task_update_matching(client, ID: str, db_dict : Matching):

    collection = client[Constants.MONGO_DB.value][Constants.MONGO_COLLECTIONS.value["coll_matching"]]

    update = db_dict.dict()
    
    filter = {"_id":ObjectId(ID)}
    
    updated = {"$set":update}
    
    result = collection.update_one(filter, updated)

    return