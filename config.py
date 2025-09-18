import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- AldiTalk Credentials ---
# These values are loaded from environment variables
PHONE_NUMBER = os.getenv("ALDI_PHONE_NUMBER")
PASSWORD = os.getenv("ALDI_PASSWORD")

# --- Telegram Bot Configuration ---
# These values are loaded from environment variables
# You can get a Bot Token by talking to @BotFather on Telegram.
# You can get your Chat ID by talking to @userinfobot.
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- Script Settings ---
# Time in seconds between each API request to refresh the data.
REQUEST_INTERVAL_SECONDS = int(os.getenv("REQUEST_INTERVAL_SECONDS", "5"))
# Time in minutes to refresh the browser page to keep the session alive.
PAGE_REFRESH_INTERVAL_MINUTES = int(os.getenv("PAGE_REFRESH_INTERVAL_MINUTES", "2"))

# Validate required environment variables
required_vars = [
    "ALDI_PHONE_NUMBER",
    "ALDI_PASSWORD", 
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID"
]

missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
