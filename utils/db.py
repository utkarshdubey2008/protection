from pymongo import MongoClient
from config import MONGO_URI


client = MongoClient(MONGO_URI)
db = client.bot_database  
groups_collection = db.groups  

def get_all_group_ids():
    """Retrieve all group chat IDs"""
    group_ids = [group["chat_id"] for group in groups_collection.find()]
    return group_ids

def add_group_to_db(chat_id):
    """Add a group to the database"""
    if not groups_collection.find_one({"chat_id": chat_id}):
        groups_collection.insert_one({"chat_id": chat_id})

def remove_group_from_db(chat_id):
    """Remove a group from the database"""
    groups_collection.delete_one({"chat_id": chat_id})
