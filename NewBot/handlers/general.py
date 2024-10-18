# general.py
from telebot import types
from utils import is_admin, get_or_create_user
from texts import (
    WELCOME_MESSAGE, LECTURES_BUTTON, ASSIGNMENTS_BUTTON,
    SUBJECTS_BUTTON, HELP_BUTTON, ADMIN_BUTTON, PDF_UTILS_BUTTON
)

def start(message, send_message_once):
    user = get_or_create_user(message.from_user.id)
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    buttons = [
        types.KeyboardButton(LECTURES_BUTTON),
        types.KeyboardButton(ASSIGNMENTS_BUTTON),
        types.KeyboardButton(SUBJECTS_BUTTON),
        types.KeyboardButton(PDF_UTILS_BUTTON),
        types.KeyboardButton(HELP_BUTTON)
    ]
    
    if is_admin(message.from_user.id):
        buttons.append(types.KeyboardButton(ADMIN_BUTTON))
    
    keyboard.add(*buttons)

    welcome_message = WELCOME_MESSAGE.format(first_name=message.from_user.first_name)
    send_message_once(message.chat.id, welcome_message, reply_markup=keyboard)