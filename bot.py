from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, LOG_GROUP_ID
from handlers.auth_handlers import authorize_user, unauthorize_user
from handlers.stats_handler import stats_command
from handlers.broadcast_handler import broadcast_message

bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_chat_member_updated()
async def log_group_addition(client, update):
    if update.chat.type in ["supergroup", "group"]:
        if update.new_chat_member.status == "member" and update.old_chat_member.status == "left":
            group_name = update.chat.title
            await bot.send_message(LOG_GROUP_ID, f"#new_group {group_name}")

@bot.on_message(filters.command(["start"]))
async def start_command(client, message):
    start_text = "Welcome to the bot! Use /help for more information. Please select an option below."
    inline_buttons = [
        [InlineKeyboardButton("Help", callback_data="help")]
    ]
    await message.reply(start_text, reply_markup=InlineKeyboardMarkup(inline_buttons))

@bot.on_message(filters.command(["help"]))
async def help_command(client, message):
    help_text = (
        "This bot offers several commands:\n\n"
        "- /start: Start the bot and receive a welcome message.\n"
        "- /auth: Authorize a user to prevent message deletion.\n"
        "- /unauth: Unauthorize a user to allow message deletion.\n"
        "- /stats: View bot statistics.\n"
        "- /broadcast: Send a message to all groups.\n\n"
        "Click the 'Close' button below to delete this message."
    )
    close_button = InlineKeyboardButton("Close", callback_data="close")
    await message.reply(help_text, reply_markup=InlineKeyboardMarkup([[close_button]]))

@bot.on_callback_query()
async def button_click_handler(client, callback_query):
    if callback_query.data == "close":
        await callback_query.message.delete()
    elif callback_query.data == "help":
        await help_command(client, callback_query.message)

@bot.on_message(filters.command(["auth"], prefixes=["/", "!"]) & filters.reply & filters.group)
async def handle_authorize_user(client, message):
    await authorize_user(client, message)

@bot.on_message(filters.command(["unauth"], prefixes=["/", "!"]) & filters.reply & filters.group)
async def handle_unauthorize_user(client, message):
    await unauthorize_user(client, message)

@bot.on_message(filters.command(["stats"], prefixes=["/", "!", "@"]) & filters.user(OWNER_ID))
async def handle_stats_command(client, message):
    await stats_command(client, message)

@bot.on_message(filters.command(["broadcast"], prefixes=["/", "!", "@"]) & filters.reply & filters.user(OWNER_ID))
async def handle_broadcast(client, message):
    await broadcast_message(client, message)

@bot.on_message(filters.command(["start"]) & filters.private)
async def log_new_user(client, message):
    user_id = message.from_user.id
    username = message.from_user.username
    await bot.send_message(LOG_GROUP_ID, f"#new_user {username} ({user_id}) started the bot")

bot.run()
