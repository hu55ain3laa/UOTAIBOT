# error_handling.py
import logging
from telebot.apihelper import ApiTelegramException
from sqlalchemy.exc import SQLAlchemyError
from texts import GENERAL_ERROR_MESSAGE, DATABASE_ERROR_MESSAGE, TELEGRAM_API_ERROR_MESSAGE

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            logger.error(f"Database error in {func.__name__}: {str(e)}")
            if 'send_message_once' in kwargs:
                kwargs['send_message_once'](args[0].chat.id, DATABASE_ERROR_MESSAGE)
            elif hasattr(args[0], 'message'):
                args[0].message.reply(DATABASE_ERROR_MESSAGE)
        except ApiTelegramException as e:
            logger.error(f"Telegram API error in {func.__name__}: {str(e)}")
            if 'send_message_once' in kwargs:
                kwargs['send_message_once'](args[0].chat.id, TELEGRAM_API_ERROR_MESSAGE)
            elif hasattr(args[0], 'message'):
                args[0].message.reply(TELEGRAM_API_ERROR_MESSAGE)
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            if 'send_message_once' in kwargs:
                kwargs['send_message_once'](args[0].chat.id, GENERAL_ERROR_MESSAGE)
            elif hasattr(args[0], 'message'):
                args[0].message.reply(GENERAL_ERROR_MESSAGE)
    return wrapper

def error_handler(bot, exception):
    logger.error(f"Unhandled exception: {str(exception)}")
    # You can add more specific handling here if needed