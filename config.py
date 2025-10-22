import os

# Telegram bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Notion integration details
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Replace this with your own Telegram chat ID after running /start once
# (The bot will print it in console so you can copy it here)
USER_ID = int(os.getenv("USER_ID", 0))
