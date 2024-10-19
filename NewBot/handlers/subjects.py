# subjects.py
from telebot import types
from sqlmodel import Session, select
from models import Subject
from database import engine
from utils import is_admin
from texts import (
    SUBJECTS_MENU, VIEW_ALL_SUBJECTS, ADD_NEW_SUBJECT, EDIT_SUBJECT,
    DELETE_SUBJECT, NO_SUBJECT_MANAGEMENT_PERMISSION, NO_SUBJECTS_AVAILABLE,
    AVAILABLE_SUBJECTS, ENTER_NEW_SUBJECT_NAME, SUBJECT_ALREADY_EXISTS,
    SUBJECT_ADDED_SUCCESSFULLY, NO_SUBJECTS_TO_EDIT, SELECT_SUBJECT_TO_EDIT,
    ENTER_NEW_SUBJECT_NAME_EDIT, SUBJECT_UPDATED_SUCCESSFULLY,
    NO_SUBJECTS_TO_DELETE, SELECT_SUBJECT_TO_DELETE, CONFIRM_SUBJECT_DELETE,
    SUBJECT_DELETED_SUCCESSFULLY, SUBJECT_DELETION_CANCELLED, SUBJECT_NOT_FOUND_ERROR
)

def subjects_menu(message, send_message_once):
    if not is_admin(message.from_user.id):
        send_message_once(message.chat.id, NO_SUBJECT_MANAGEMENT_PERMISSION)
        return
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton(VIEW_ALL_SUBJECTS, callback_data="view_subjects"))
    keyboard.row(types.InlineKeyboardButton(ADD_NEW_SUBJECT, callback_data="add_subject"))
    keyboard.row(types.InlineKeyboardButton(EDIT_SUBJECT, callback_data="edit_subject"))
    keyboard.row(types.InlineKeyboardButton(DELETE_SUBJECT, callback_data="delete_subject"))
    send_message_once(message.chat.id, SUBJECTS_MENU, reply_markup=keyboard)

def view_subjects(call, send_message_once):
    with Session(engine) as session:
        subjects = session.exec(select(Subject)).all()
    
    if not subjects:
        send_message_once(call.message.chat.id, NO_SUBJECTS_AVAILABLE)
        return

    subject_list = AVAILABLE_SUBJECTS
    for subject in subjects:
        subject_list += f"- {subject.name}\n"
    send_message_once(call.message.chat.id, subject_list)

def add_subject_prompt(call, send_message_once, bot):
    message = send_message_once(call.message.chat.id, ENTER_NEW_SUBJECT_NAME)
    bot.register_next_step_handler(message, save_new_subject, send_message_once)

def save_new_subject(message, send_message_once):
    subject_name = message.text.strip()
    with Session(engine) as session:
        existing_subject = session.exec(select(Subject).where(Subject.name == subject_name)).first()
        if existing_subject:
            send_message_once(message.chat.id, SUBJECT_ALREADY_EXISTS.format(subject_name=subject_name))
        else:
            new_subject = Subject(name=subject_name)
            session.add(new_subject)
            session.commit()
            send_message_once(message.chat.id, SUBJECT_ADDED_SUCCESSFULLY.format(subject_name=subject_name))

def edit_subject_prompt(call, send_message_once):
    with Session(engine) as session:
        subjects = session.exec(select(Subject)).all()
    
    if not subjects:
        send_message_once(call.message.chat.id, NO_SUBJECTS_TO_EDIT)
        return

    keyboard = types.InlineKeyboardMarkup()
    for subject in subjects:
        keyboard.add(types.InlineKeyboardButton(subject.name, callback_data=f"edit_subject_{subject.id}"))
    send_message_once(call.message.chat.id, SELECT_SUBJECT_TO_EDIT, reply_markup=keyboard)

def edit_subject(call, send_message_once, bot):
    subject_id = int(call.data.split("_")[-1])
    message = send_message_once(call.message.chat.id, ENTER_NEW_SUBJECT_NAME_EDIT)
    bot.register_next_step_handler(message, save_edited_subject, subject_id, send_message_once)

def save_edited_subject(message, subject_id, send_message_once):
    new_name = message.text.strip()
    with Session(engine) as session:
        subject = session.get(Subject, subject_id)
        if subject:
            subject.name = new_name
            session.commit()
            send_message_once(message.chat.id, SUBJECT_UPDATED_SUCCESSFULLY.format(new_name=new_name))
        else:
            send_message_once(message.chat.id, SUBJECT_NOT_FOUND_ERROR)

def delete_subject_prompt(call, send_message_once):
    with Session(engine) as session:
        subjects = session.exec(select(Subject)).all()
    
    if not subjects:
        send_message_once(call.message.chat.id, NO_SUBJECTS_TO_DELETE)
        return

    keyboard = types.InlineKeyboardMarkup()
    for subject in subjects:
        keyboard.add(types.InlineKeyboardButton(subject.name, callback_data=f"delete_subject_{subject.id}"))
    send_message_once(call.message.chat.id, SELECT_SUBJECT_TO_DELETE, reply_markup=keyboard)

def delete_subject_confirm(call, send_message_once):
    subject_id = int(call.data.split("_")[-1])
    with Session(engine) as session:
        subject = session.get(Subject, subject_id)
        if subject:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(
                types.InlineKeyboardButton("نعم", callback_data=f"confirm_delete1_{subject_id}"),
                types.InlineKeyboardButton("لا", callback_data="cancel_delete")
            )
            send_message_once(call.message.chat.id, CONFIRM_SUBJECT_DELETE.format(subject_name=subject.name), reply_markup=keyboard)
        else:
            send_message_once(call.message.chat.id, SUBJECT_NOT_FOUND_ERROR)

def delete_subject(call, send_message_once):
    subject_id = int(call.data.split("_")[-1])
    with Session(engine) as session:
        subject = session.get(Subject, subject_id)
        if subject:
            session.delete(subject)
            session.commit()
            send_message_once(call.message.chat.id, SUBJECT_DELETED_SUCCESSFULLY.format(subject_name=subject.name))
        else:
            send_message_once(call.message.chat.id, SUBJECT_NOT_FOUND_ERROR)

def cancel_delete(call, send_message_once):
    send_message_once(call.message.chat.id, SUBJECT_DELETION_CANCELLED)