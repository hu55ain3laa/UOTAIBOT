# main.py
import os
import logging
from dotenv import load_dotenv
from telebot import TeleBot
from telebot.types import Message
from database import init_db
from handlers import register_handlers
from utils import send_message_once

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = TeleBot("7426713797:AAE1CQOOlf40Ff47jtXO4VAtX7umfTTSH38")

# Initialize database
try:
    init_db()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database: {str(e)}")
    exit(1)

# Create send_message_once function with bot instance
send_message_once_with_bot = lambda *args, **kwargs: send_message_once(bot, *args, **kwargs)

# Register all handlers
register_handlers(bot, send_message_once_with_bot)

# Test handler to check if the bot is responding
@bot.message_handler(commands=['test'])
def test_handler(message: Message):
    logger.info(f"Received test command from user {message.from_user.id}")
    bot.reply_to(message, "Bot is working!")

# Main execution
if __name__ == "__main__":
    logger.info("Starting the bot...")
    bot.remove_webhook()
    logger.info("Bot is now polling for updates...")
    
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            logger.error(f"Error in main polling loop: {str(e)}")
            continue