from pyrogram import Client
import pyrogram
from config import API_ID, API_HASH, BOT_TOKEN
from sqlmodel import SQLModel, create_engine
from config import DATABASE_URL
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers import send_daily_update
import asyncio

# Create SQLite engine
engine = create_engine(DATABASE_URL)

# Create tables
SQLModel.metadata.create_all(engine)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a client using your bot token
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

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

# Set up scheduler for daily updates
scheduler = AsyncIOScheduler()
scheduler.add_job(send_daily_update, 'cron', hour=8, args=[app])  # Send update every day at 8 AM

async def main():
    await app.start()
    user_me = await app.get_me()
    print(f"Bot started as {user_me.first_name}")
    
    scheduler.start()
    
    # Run the client until you press Ctrl+C
    await pyrogram.idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(app.stop())
        loop.close()