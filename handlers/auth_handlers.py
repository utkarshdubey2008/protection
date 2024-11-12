from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
from config import MONGO_URI

client_db = MongoClient(MONGO_URI)
db = client_db["bot_database"]
users_collection = db["authorized_users"]

async def authorize_user(client: Client, message: Message):
    user = message.reply_to_message.from_user
    if users_collection.find_one({"user_id": user.id}):
        await message.reply(f"User @{user.username} is already authorized.")
    else:
        users_collection.insert_one({"user_id": user.id, "username": user.username})
        await message.reply(f"User @{user.username} has been authorized.")

async def unauthorize_user(client: Client, message: Message):
    user = message.reply_to_message.from_user
    if users_collection.find_one({"user_id": user.id}):
        users_collection.delete_one({"user_id": user.id})
        await message.reply(f"User @{user.username} has been unauthorized.")
    else:
        await message.reply(f"User @{user.username} is not authorized.")
