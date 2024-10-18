import os
from dotenv import load_dotenv
from telebot import TeleBot
from database import init_db
from handlers import register_handlers
from utils import send_message_once

# Load environment variables

# Initialize bot
bot = TeleBot("7426713797:AAE1CQOOlf40Ff47jtXO4VAtX7umfTTSH38")

# Initialize database
init_db()

# Create send_message_once function with bot instance
send_message_once_with_bot = lambda *args, **kwargs: send_message_once(bot, *args, **kwargs)

# Register all handlers
register_handlers(bot, send_message_once_with_bot)


# Main execution
if __name__ == "__main__":
    print("Starting the bot...")
    bot.remove_webhook()
    print("Bot is now polling for updates...")
    bot.polling(none_stop=True, interval=0, timeout=20)