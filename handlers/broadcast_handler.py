# handlers/broadcast_handler.py

from pyrogram import Client
from pyrogram.types import Message
from utils.db import get_all_user_ids, get_all_group_ids

async def broadcast_message(client: Client, message: Message):
    """Broadcasts a message to all users and groups"""
    if message.from_user.id != OWNER_ID:
        await message.reply("You are not authorized to use this command.")
        return


    if len(message.text.split(" ", 1)) < 2:
        await message.reply("Please provide a message to broadcast.")
        return
    
    broadcast_text = message.text.split(" ", 1)[1]

    
    user_ids = get_all_user_ids()
    group_ids = get_all_group_ids()

    if not user_ids and not group_ids:
        await message.reply("No users or groups found to broadcast the message.")
        return

    # Broadcast to users
    for user_id in user_ids:
        try:
            await client.send_message(user_id, broadcast_text)
        except Exception as e:
            print(f"Failed to send message to user {user_id}: {e}")

    # Broadcasting to groups 
    for group_id in group_ids:
        try:
            await client.send_message(group_id, broadcast_text)
        except Exception as e:
            print(f"Failed to send message to group {group_id}: {e}")
    
    await message.reply(f"Broadcast message sent to {len(user_ids)} users and {len(group_ids)} groups.")
