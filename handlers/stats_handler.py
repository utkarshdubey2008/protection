from pyrogram import Client
from pyrogram.types import Message
from utils.db import get_all_user_ids, get_all_group_ids

async def show_stats(client: Client, message: Message):
    """Show bot statistics like number of users and active groups"""
    user_count = len(get_all_user_ids())
    group_count = len(get_all_group_ids())

    stats_text = f"Bot Stats:\n\nUsers who started the bot: {user_count}\nActive Groups: {group_count}"
    
    await message.reply(stats_text)
