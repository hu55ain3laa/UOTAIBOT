# utils.py
from sqlmodel import Session, select
from models import User
from database import engine
from telebot import TeleBot
from telebot.types import Message

processed_items = {}

def is_admin(user_id: int) -> bool:
    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_id == user_id)).first()
        if user.is_admin == True:
            return True
        else:
            return False

def is_admin_local(user_id: int) -> bool:
    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_id == user_id)).first()
        if user.is_admin == True:
            return True
        else:
            return False

def get_or_create_user(telegram_id: int) -> User:
    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_id == telegram_id)).first()
        if not user:
            user = User(telegram_id=telegram_id)
            session.add(user)
            session.commit()
            session.refresh(user)
        return user

def send_message_once(bot: TeleBot, chat_id: int, text: str, **kwargs):
    if 'document' in kwargs:
        document = kwargs.pop('document')
        message = bot.send_document(chat_id, document, caption=text, **kwargs)
    else:
        message = bot.send_message(chat_id, text, **kwargs)
    processed_items[f"msg_{message.message_id}"] = True
    return message

def prevent_duplicate_message(func):
    def wrapper(message):
        if f"msg_{message.message_id}" not in processed_items:
            processed_items[f"msg_{message.message_id}"] = True
            return func(message)
    return wrapper

def prevent_duplicate_callback(func):
    def wrapper(call):
        if f"call_{call.id}" not in processed_items:
            processed_items[f"call_{call.id}"] = True
            return func(call)
    return wrapper

def safe_register_next_step(bot: TeleBot, message: Message, handler, function_name: str):
    if handler is not None and callable(handler):
        bot.register_next_step_handler(message, handler)
    else:
        print(f"Warning: Invalid next step handler for message {message.message_id} in function {function_name}")

def get_or_create_user(telegram_id: int, name: str = None) -> User:
    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_id == telegram_id)).first()
        if not user:
            user = User(telegram_id=telegram_id, name=name or f"User_{telegram_id}")
            session.add(user)
            session.commit()
            session.refresh(user)
        elif name and user.name != name:
            user.name = name
            session.commit()
            session.refresh(user)
        return user
    