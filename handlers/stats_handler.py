from utils.db import get_stats

# Handle the stats command (Owner only)
async def stats_command(client, message):
    total_users, total_groups = get_stats()
    stats_text = (
        f"Bot Stats:\n\n"
        f"Total Users: {total_users}\n"
        f"Total Groups: {total_groups}"
    )
    await message.reply(stats_text)
