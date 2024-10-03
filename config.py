from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get values from environment variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

# Database configuration
DATABASE_URL = "sqlite:///users.db"