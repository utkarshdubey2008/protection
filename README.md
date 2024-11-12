

# Telegram Bot

This is a Python-based Telegram bot that supports various features like message deletion based on word count, edited messages, user authorization, and broadcasting messages across groups. Additionally, it allows interaction with a database (MongoDB) and includes owner-specific commands like `/stats` and `/broadcast`.

## Features

1. **Message Deletion**:
   - Deletes messages that contain more than 200 words.
   - Deletes messages that are edited after 2 minutes.

2. **User Authorization**:
   - Admins can authorize/unauthorize users in the group using `/auth` and `/unauth` commands.
   - Authorized users' messages will not be deleted, while unauthenticated users' messages will be deleted.

3. **Commands**:
   - **`/start`**: Sends a welcome message and displays inline buttons (details will be added later).
   - **`/help`**: Provides a description of the `/start` command with a close button.
   - **`/auth`**: Allows admins to authorize a user in the group (available via `/` or `!`).
   - **`/unauth`**: Allows admins to unauthorize a user in the group (available via `/` or `!`).
   - **`/stats`**: Displays bot statistics, available to the owner only.
   - **`/broadcast`**: Broadcasts a message to all groups the bot is in, and users who have started the bot (owner only).

4. **Log Group Integration**:
   - Every time the bot is added to a new group or a new user starts the bot, a notification is sent to a designated log group with their data and a hashtag `#new_user` or `#new_group`.

## Installation

### Requirements

- Python 3.7 or higher
- `pyrogram` library for interacting with the Telegram API
- MongoDB for storing data

### Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/telegram-bot.git
   cd telegram-bot

2. Install the required dependencies:

pip install -r requirements.txt


3. Create a .env file in the root directory of the project to store sensitive information like your bot token, MongoDB URL, etc. Example:

API_ID=<Your API ID>
API_HASH=<Your API HASH>
BOT_TOKEN=<Your Bot Token>
OWNER_ID=<Your Owner ID>
LOG_GROUP_ID=<Your Log Group ID>


4. Run the bot:

python bot.py



Commands

/start

Displays a custom welcome message with inline buttons.

More details about the buttons will be added later.


/help

Displays help information about the bot, including what the /start command does.

Includes an inline "Close" button to delete the message.


/auth (Group Admin Only)

Authorizes a user, preventing their messages from being deleted.

Usage: Reply to the user with the /auth command.


/unauth (Group Admin Only)

Unauthorizes a user, causing their messages to be deleted.

Usage: Reply to the user with the /unauth command.


/stats (Owner Only)

Displays bot statistics, such as the number of users and groups the bot is in.


/broadcast (Owner Only)

Broadcasts a message to all groups the bot is in and all users who have started the bot.

Usage: Reply to a message with the /broadcast command.


Log Group Integration

Whenever the bot is added to a new group or a new user starts the bot, a notification is sent to the log group with the respective data:

If a user starts the bot: #new_user <user_id>

If the bot is added to a new group: #new_group <group_name>


Contributing

Feel free to fork this project and submit pull requests. If you find any bugs or have suggestions, please open an issue.

License

This project is licensed under the MIT License.

### Updated Features in the Code:

1. **`/start` and `/help` Commands**: 
   - The `/start` command will show a custom start message and inline buttons. You can modify the exact content of the inline buttons later.
   - The `/help` command will display information about the `/start` command and will also include an inline "Close" button to delete the help message.

2. **Log Group Notification**:
   - When the bot is added to a new group or a new user starts the bot, a notification is sent to a log group (defined in the configuration) with a message in the format `#new_user <user_id>` or `#new_group <group_name>`.

### Code Changes for `/start`, `/help`, and Log Group

Here's an update to the `bot.py` to handle the `/start`, `/help`, and log group notifications:

```python
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, LOG_GROUP_ID
from handlers.auth_handlers import authorize_user, unauthorize_user
from handlers.stats_handler import stats_command
from handlers.broadcast_handler import broadcast_message

bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Log new group or user
@bot.on_chat_member_updated()
async def log_group_addition(client, update):
    if update.chat.type in ["supergroup", "group"]:
        if update.new_chat_member.status == "member" and update.old_chat_member.status == "left":
            group_name = update.chat.title
            await bot.send_message(LOG_GROUP_ID, f"#new_group {group_name}")

@bot.on_message(filters.command(["start"]))
async def start_command(client, message):
    await message.reply("Welcome to the bot! Use /help for more information.", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Help", callback_data="help")]
    ]))

@bot.on_message(filters.command(["help"]))
async def help_command(client, message):
    help_text = "This bot has several commands. Use /start to begin. For assistance, use /help."
    close_button = InlineKeyboardButton("Close", callback_data="close")
    await message.reply(help_text, reply_markup=InlineKeyboardMarkup([[close_button]]))

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

bot.run()

Key Updates:

log_group_addition: Monitors when a bot is added to a new group and sends a log to a designated log group.

/start: Sends a custom welcome message with inline buttons.

/help: Provides help text with a "Close" button.


