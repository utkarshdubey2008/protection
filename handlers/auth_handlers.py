from pyrogram import Client, filters
from pyrogram.types import Message

async def authorize_user(client: Client, message: Message):
    user = message.reply_to_message.from_user
    await message.reply(f"User {user.username} has been authorized.")

async def unauthorize_user(client: Client, message: Message):
    user = message.reply_to_message.from_user
    await message.reply(f"User {user.username} has been unauthorized.")
