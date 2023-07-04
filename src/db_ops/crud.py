from bson import ObjectId

from src.constants import Constants

from .schemas import Matching, Extraction

def status_add(client, coll_name : str, status : str):
    """Function to add the record of status at the beginning of the task in the database"""

    collection = client[Constants.MONGO_DB.value][coll_name]

    record = {"status":status}

    db_item = collection.insert_one(record)

    return str(db_item.inserted_id)

def status_update(client,coll_name : str, status:str, ID:str):
    """Function to update the status of database"""
    collection = client[Constants.MONGO_DB.value][coll_name]

    update = {"status":status}

    filter = {"_id":ObjectId(ID)}

    updated_status = {"$set":update}

    result = collection.update_one(filter, updated_status)

    return

def task_update_extraction(client, ID: str, db_dict : Extraction):
    '''This function will update the extraction task in the database'''

    collection = client[Constants.MONGO_DB.value][Constants.MONGO_COLLECTIONS.value["coll_extraction"]]

    update = db_dict.dict()
    
    filter = {"_id":ObjectId(ID)}
    
    updated = {"$set":update}
    
    result = collection.update_one(filter, updated)

    return

def task_update_matching(client, ID: str, db_dict : Matching):
    '''This function will update the matching task in the database'''

    collection = client[Constants.MONGO_DB.value][Constants.MONGO_COLLECTIONS.value["coll_matching"]]

    update = db_dict.dict()
    
    filter = {"_id":ObjectId(ID)}
    
    updated = {"$set":update}
    
    result = collection.update_one(filter, updated)

    return