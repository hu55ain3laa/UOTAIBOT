from sqlmodel import SQLModel, create_engine
from config import DATABASE_URL
import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
# Create SQLite engine
engine = create_engine(DATABASE_URL)

# Create tables
SQLModel.metadata.create_all(engine)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import handlers
from handlers import *

# Global error handler
@app.on_raw_update()
async def global_error_handler(client, update, users, chats):
    try:
        # Handle raw updates here
        pass
    except Exception as e:
        logging.error(f"An error occurred in global_error_handler: {e}")

if __name__ == "__main__":
    app.run()