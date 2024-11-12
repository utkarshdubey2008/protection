import logging
from pymongo import MongoClient
from config import MONGO_URI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = MongoClient(MONGO_URI)
db = client.bot_database
groups_collection = db.groups

def get_all_group_ids():
    """Retrieve all group chat IDs"""
    try:
        group_ids = [group["chat_id"] for group in groups_collection.find()]
        return group_ids
    except Exception as e:
        logger.error(f"Error getting group IDs: {e}")
        return []

def add_group_to_db(chat_id):
    """Add a group to the database"""
    try:
        # Using upsert to avoid duplicate entries
        groups_collection.update_one({"chat_id": chat_id}, {"$set": {"chat_id": chat_id}}, upsert=True)
        logger.info(f"Group {chat_id} added to database.")
    except Exception as e:
        logger.error(f"Error adding group to database: {e}")

def remove_group_from_db(chat_id):
    """Remove a group from the database"""
    try:
        result = groups_collection.delete_one({"chat_id": chat_id})
        if result.deleted_count > 0:
            logger.info(f"Group {chat_id} removed from database.")
        else:
            logger.warning(f"No group found with chat_id {chat_id}")
    except Exception as e:
        logger.error(f"Error removing group from database: {e}")
