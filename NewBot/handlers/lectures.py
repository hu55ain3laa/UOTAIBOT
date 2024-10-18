from telebot import types
from utils import is_admin
from sqlmodel import Session, select
from models import Lecture, Subject, User
from database import engine
from texts import (
    LECTURES_MENU, SUBJECT_NOT_FOUND_ERROR, USER_NOT_FOUND_ERROR, VIEW_LECTURES_BY_SUBJECT, UPLOAD_NEW_LECTURE,
    NO_SUBJECTS_AVAILABLE, SELECT_SUBJECT_VIEW_LECTURES, SUBJECT_NOT_FOUND,
    NO_LECTURES_AVAILABLE, SUBJECT_LECTURES_HEADER, LECTURE_INFO,
    NO_UPLOAD_PERMISSION, NO_SUBJECTS_ADD_FIRST, SELECT_SUBJECT_NEW_LECTURE,
    ENTER_LECTURE_NUMBER, INVALID_LECTURE_NUMBER, ENTER_LECTURE_TITLE,
    SEND_LECTURE_FILE, LECTURE_ADDED_SUCCESSFULLY, SUBJECT_NOT_FOUND_LECTURE_NOT_SAVED,
    SEND_LECTURE_FILE_PROMPT, EDIT_LECTURE, DELETE_LECTURE, SELECT_LECTURE_TO_EDIT,
    SELECT_LECTURE_TO_DELETE, NO_LECTURES_TO_EDIT, NO_LECTURES_TO_DELETE,
    ENTER_NEW_LECTURE_TITLE, LECTURE_UPDATED_SUCCESSFULLY, CONFIRM_LECTURE_DELETE,
    LECTURE_DELETED_SUCCESSFULLY, LECTURE_DELETION_CANCELLED
)

def lectures_menu(message, send_message_once):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton(VIEW_LECTURES_BY_SUBJECT, callback_data="view_lectures_subjects"))
    if is_admin(message.from_user.id):
        keyboard.row(types.InlineKeyboardButton(UPLOAD_NEW_LECTURE, callback_data="upload_lecture"))
        keyboard.row(types.InlineKeyboardButton(EDIT_LECTURE, callback_data="edit_lecture"))
        keyboard.row(types.InlineKeyboardButton(DELETE_LECTURE, callback_data="delete_lecture"))
    send_message_once(message.chat.id, LECTURES_MENU, reply_markup=keyboard)

def view_lectures_subjects(call, send_message_once):
    with Session(engine) as session:
        subjects = session.exec(select(Subject).order_by(Subject.name)).all()
    
    if not subjects:
        send_message_once(call.message.chat.id, NO_SUBJECTS_AVAILABLE)
        return

    keyboard = types.InlineKeyboardMarkup()
    for subject in subjects:
        keyboard.add(types.InlineKeyboardButton(subject.name, callback_data=f"view_lectures_{subject.id}"))
    
    send_message_once(call.message.chat.id, SELECT_SUBJECT_VIEW_LECTURES, reply_markup=keyboard)

def view_lectures(call, send_message_once):
    subject_id = int(call.data.split("_")[-1])
    with Session(engine) as session:
        subject = session.get(Subject, subject_id)
        if not subject:
            send_message_once(call.message.chat.id, SUBJECT_NOT_FOUND)
            return
        
        lectures = session.exec(select(Lecture).where(Lecture.subject_id == subject_id).order_by(Lecture.lecture_number)).all()
        
        if not lectures:
            send_message_once(call.message.chat.id, NO_LECTURES_AVAILABLE.format(subject_name=subject.name))
            return

        send_message_once(call.message.chat.id, SUBJECT_LECTURES_HEADER.format(subject_name=subject.name))
        for lecture in lectures:
            lecture_text = LECTURE_INFO.format(lecture_number=lecture.lecture_number, title=lecture.title)
            send_message_once(call.message.chat.id, lecture_text, document=lecture.file_id)

def upload_lecture_prompt(call, send_message_once):
    if not is_admin(call.from_user.id):
        send_message_once(call.message.chat.id, NO_UPLOAD_PERMISSION)
        return
    
    with Session(engine) as session:
        subjects = session.exec(select(Subject)).all()
    if not subjects:
        send_message_once(call.message.chat.id, NO_SUBJECTS_ADD_FIRST)
        return

    keyboard = types.InlineKeyboardMarkup()
    for subject in subjects:
        keyboard.add(types.InlineKeyboardButton(subject.name, callback_data=f"select_subject_{subject.id}"))
    send_message_once(call.message.chat.id, SELECT_SUBJECT_NEW_LECTURE, reply_markup=keyboard)

def process_lecture_number(message, send_message_once):
    try:
        lecture_number = int(message.text)
        with Session(engine) as session:
            user = session.exec(select(User).where(User.telegram_id == message.from_user.id)).first()
            if user:
                user.temp_lecture_number = lecture_number
                user.lecture_state = 'waiting_for_title'
                session.commit()
                send_message_once(message.chat.id, ENTER_LECTURE_TITLE)
            else:
                send_message_once(message.chat.id, USER_NOT_FOUND_ERROR)
    except ValueError:
        send_message_once(message.chat.id, INVALID_LECTURE_NUMBER)

def process_lecture_subject(call, send_message_once):
    subject_id = int(call.data.split("_")[-1])
    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_id == call.from_user.id)).first()
        if not user:
            user = User(telegram_id=call.from_user.id)
            session.add(user)
        user.temp_subject_id = subject_id
        user.lecture_state = 'waiting_for_number'
        user.assignment_state = None  # Clear assignment state
        session.commit()
    
    send_message_once(call.message.chat.id, ENTER_LECTURE_NUMBER)

def handle_lecture_steps(message, send_message_once):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_id == message.from_user.id)).first()
        if not user or not user.lecture_state:
            return False

        if user.lecture_state == 'waiting_for_number':
            process_lecture_number(message, send_message_once)
        elif user.lecture_state == 'waiting_for_title':
            process_lecture_title(message, user.temp_subject_id, user.temp_lecture_number, send_message_once)
        elif user.lecture_state == 'waiting_for_file':
            save_lecture(message, user.temp_subject_id, user.temp_lecture_number, user.temp_lecture_title, send_message_once)
        
        return True

def process_lecture_title(message, subject_id, lecture_number, send_message_once):
    title = message.text
    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_id == message.from_user.id)).first()
        user.temp_lecture_title = title
        user.lecture_state = 'waiting_for_file'
        session.commit()
    
    send_message_once(message.chat.id, SEND_LECTURE_FILE)

def save_lecture(message, subject_id, lecture_number, title, send_message_once):
    if message.document:
        file_id = message.document.file_id
        with Session(engine) as session:
            subject = session.get(Subject, subject_id)
            if subject:
                lecture = Lecture(subject_id=subject_id, lecture_number=lecture_number, title=title, file_id=file_id)
                session.add(lecture)
                user = session.exec(select(User).where(User.telegram_id == message.from_user.id)).first()
                user.lecture_state = None
                user.temp_subject_id = None
                user.temp_lecture_number = None
                user.temp_lecture_title = None
                session.commit()
                send_message_once(message.chat.id, LECTURE_ADDED_SUCCESSFULLY.format(title=title, lecture_number=lecture_number, subject_name=subject.name))
            else:
                send_message_once(message.chat.id, SUBJECT_NOT_FOUND_LECTURE_NOT_SAVED)
    else:
        send_message_once(message.chat.id, SEND_LECTURE_FILE_PROMPT)

def edit_lecture_prompt(call, send_message_once):
    if not is_admin(call.from_user.id):
        send_message_once(call.message.chat.id, NO_UPLOAD_PERMISSION)
        return

    with Session(engine) as session:
        lectures = session.exec(select(Lecture).order_by(Lecture.subject_id, Lecture.lecture_number)).all()

    if not lectures:
        send_message_once(call.message.chat.id, NO_LECTURES_TO_EDIT)
        return

    keyboard = types.InlineKeyboardMarkup()
    for lecture in lectures:
        subject = session.get(Subject, lecture.subject_id)
        button_text = f"{subject.name} - {lecture.lecture_number}: {lecture.title}"
        keyboard.add(types.InlineKeyboardButton(button_text, callback_data=f"edit_lecture_{lecture.id}"))
    
    send_message_once(call.message.chat.id, SELECT_LECTURE_TO_EDIT, reply_markup=keyboard)

def edit_lecture(call, send_message_once, bot):
    lecture_id = int(call.data.split("_")[-1])
    with Session(engine) as session:
        lecture = session.get(Lecture, lecture_id)
        if lecture:
            message = send_message_once(call.message.chat.id, ENTER_NEW_LECTURE_TITLE)
            bot.register_next_step_handler(message, save_edited_lecture, lecture_id, send_message_once)
        else:
            send_message_once(call.message.chat.id, SUBJECT_NOT_FOUND_ERROR)

def save_edited_lecture(message, lecture_id, send_message_once):
    new_title = message.text.strip()
    with Session(engine) as session:
        lecture = session.get(Lecture, lecture_id)
        if lecture:
            lecture.title = new_title
            session.commit()
            send_message_once(message.chat.id, LECTURE_UPDATED_SUCCESSFULLY.format(new_title=new_title))
        else:
            send_message_once(message.chat.id, SUBJECT_NOT_FOUND_ERROR)

def delete_lecture_prompt(call, send_message_once):
    if not is_admin(call.from_user.id):
        send_message_once(call.message.chat.id, NO_UPLOAD_PERMISSION)
        return

    with Session(engine) as session:
        lectures = session.exec(select(Lecture).order_by(Lecture.subject_id, Lecture.lecture_number)).all()

    if not lectures:
        send_message_once(call.message.chat.id, NO_LECTURES_TO_DELETE)
        return

    keyboard = types.InlineKeyboardMarkup()
    for lecture in lectures:
        subject = session.get(Subject, lecture.subject_id)
        button_text = f"{subject.name} - {lecture.lecture_number}: {lecture.title}"
        keyboard.add(types.InlineKeyboardButton(button_text, callback_data=f"delete_lecture_{lecture.id}"))
    
    send_message_once(call.message.chat.id, SELECT_LECTURE_TO_DELETE, reply_markup=keyboard)

def delete_lecture_confirm(call, send_message_once):
    lecture_id = int(call.data.split("_")[-1])
    with Session(engine) as session:
        lecture = session.get(Lecture, lecture_id)
        if lecture:
            subject = session.get(Subject, lecture.subject_id)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(
                types.InlineKeyboardButton("نعم", callback_data=f"confirm_delete_lecture_{lecture_id}"),
                types.InlineKeyboardButton("لا", callback_data="cancel_delete_lecture")
            )
            confirm_message = CONFIRM_LECTURE_DELETE.format(
                subject_name=subject.name,
                lecture_number=lecture.lecture_number,
                lecture_title=lecture.title
            )
            send_message_once(call.message.chat.id, confirm_message, reply_markup=keyboard)
        else:
            send_message_once(call.message.chat.id, SUBJECT_NOT_FOUND_ERROR)

def delete_lecture(call, send_message_once):
    lecture_id = int(call.data.split("_")[-1])
    with Session(engine) as session:
        lecture = session.get(Lecture, lecture_id)
        if lecture:
            subject = session.get(Subject, lecture.subject_id)
            session.delete(lecture)
            session.commit()
            success_message = LECTURE_DELETED_SUCCESSFULLY.format(
                subject_name=subject.name,
                lecture_number=lecture.lecture_number,
                lecture_title=lecture.title
            )
            send_message_once(call.message.chat.id, success_message)
        else:
            send_message_once(call.message.chat.id, SUBJECT_NOT_FOUND_ERROR)

def cancel_delete_lecture(call, send_message_once):
    send_message_once(call.message.chat.id, LECTURE_DELETION_CANCELLED)