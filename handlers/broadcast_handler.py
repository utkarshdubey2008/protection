from pyrogram import Client
from pyrogram.types import Message
from utils.db import get_all_group_ids

async def broadcast_message(client: Client, message: Message):
    """Broadcasts a message to all groups (Owner only)"""
    
    if message.from_user.id != OWNER_ID:
        await message.reply("You are not authorized to use this command.")
        return
    
    # Get message to broadcast
    if len(message.text.split(" ", 1)) < 2:
        await message.reply("Please provide the message text to broadcast.")
        return
    
    broadcast_text = message.text.split(" ", 1)[1]

    # For getting group id and broadcasting 
    group_ids = get_all_group_ids()
    
    if not group_ids:
        await message.reply("No groups found to broadcast the message.")
        return

    for group_id in group_ids:
        try:
            await client.send_message(group_id, broadcast_text)
        except Exception as e:
            print(f"Failed to send message to group {group_id}: {e}")
    
    await message.reply(f"Broadcast message sent to {len(group_ids)} groups.")
