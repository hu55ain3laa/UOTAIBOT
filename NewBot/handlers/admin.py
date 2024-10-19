# admin.py
from telebot import types
from sqlmodel import Session, select
from models import User
from database import engine
from utils import is_admin
from telebot.types import Message
import os
from telebot import TeleBot
from dotenv import load_dotenv
from texts import (
    ADMIN_MENU, LIST_USERS, ADD_ADMIN, REMOVE_ADMIN, NO_ADMIN_PERMISSION,
    MAKE_ADMIN_USAGE, INCORRECT_PASSWORD, ALREADY_ADMIN, NOW_ADMIN,
    ADDED_AS_ADMIN, NO_PERMISSION_LIST_USERS, TELEGRAM_API_ERROR, USER_LIST_HEADER,
    USER_INFO, NO_PERMISSION_MODIFY_ADMIN, ENTER_TELEGRAM_ID,
    INVALID_TELEGRAM_ID, USER_NOT_FOUND, ADMIN_STATUS_CHANGED, USERNAME_RESULT, USERNAME_USAGE
)

load_dotenv()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

def admin_menu(message, send_message_once):
    if not is_admin(message.from_user.id):
        send_message_once(message.chat.id, NO_ADMIN_PERMISSION)
        return

    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton(LIST_USERS, callback_data="list_users"))
    keyboard.row(types.InlineKeyboardButton(ADD_ADMIN, callback_data="add_admin"))
    keyboard.row(types.InlineKeyboardButton(REMOVE_ADMIN, callback_data="remove_admin"))
    send_message_once(message.chat.id, ADMIN_MENU, reply_markup=keyboard)

def make_admin(message, send_message_once):
    command_parts = message.text.split()
    if len(command_parts) != 2:
        send_message_once(message.chat.id, MAKE_ADMIN_USAGE)
        return

    password = command_parts[1]
    if password != "X@2":
        send_message_once(message.chat.id, INCORRECT_PASSWORD)
        return

    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_id == message.from_user.id)).first()
        if user:
            if user.is_admin:
                send_message_once(message.chat.id, ALREADY_ADMIN)
            else:
                user.is_admin = True
                session.commit()
                send_message_once(message.chat.id, NOW_ADMIN)
        else:
            new_user = User(telegram_id=message.from_user.id, is_admin=True)
            session.add(new_user)
            session.commit()
            send_message_once(message.chat.id, ADDED_AS_ADMIN)

def list_users(call, send_message_once):
    if not is_admin(call.from_user.id):
        send_message_once(call.message.chat.id, NO_PERMISSION_LIST_USERS)
        return

    with Session(engine) as session:
        users = session.exec(select(User)).all()
    
    user_list = USER_LIST_HEADER
    for user in users:
        user_list += USER_INFO.format(
            id=user.id,
            telegram_id=user.telegram_id,
            is_admin="نعم" if user.is_admin else "لا"
        )
    
    send_message_once(call.message.chat.id, user_list)

def admin_action_prompt(call, send_message_once):
    if not is_admin(call.from_user.id):
        send_message_once(call.message.chat.id, NO_PERMISSION_MODIFY_ADMIN)
        return

    action = "إضافة" if call.data == "add_admin" else "إزالة"
    send_message_once(call.message.chat.id, ENTER_TELEGRAM_ID.format(action=action))
    return lambda m: process_admin_action(m, action, send_message_once)

def process_admin_action(message, action, send_message_once):
    try:
        target_id = int(message.text)
    except ValueError:
        send_message_once(message.chat.id, INVALID_TELEGRAM_ID)
        return

    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_id == target_id)).first()
        if not user:
            send_message_once(message.chat.id, USER_NOT_FOUND.format(target_id=target_id))
            return

        user.is_admin = (action == "إضافة")
        session.commit()

    status = "كـ" if action == "إضافة" else "من"
    send_message_once(message.chat.id, ADMIN_STATUS_CHANGED.format(action=action, target_id=target_id, status=status))

def get_username_by_id(message: Message, send_message_once, bot: TeleBot):
    if not is_admin(message.from_user.id):
        send_message_once(message.chat.id, NO_ADMIN_PERMISSION)
        return

    command_parts = message.text.split()
    if len(command_parts) != 2:
        send_message_once(message.chat.id, USERNAME_USAGE)
        return

    try:
        target_id = int(command_parts[1])
    except ValueError:
        send_message_once(message.chat.id, USERNAME_USAGE)
        return

    try:
        chat = bot.get_chat(target_id)
        username = chat.username or "لا يوجد اسم مستخدم"
        first_name = chat.first_name or "لا يوجد اسم أول"
        last_name = chat.last_name or "لا يوجد اسم أخير"
        
        response = USERNAME_RESULT.format(
            id=target_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        send_message_once(message.chat.id, response)
    except Exception as e:
        if "user not found" in str(e).lower():
            send_message_once(message.chat.id, USER_NOT_FOUND)
        else:
            send_message_once(message.chat.id, TELEGRAM_API_ERROR)