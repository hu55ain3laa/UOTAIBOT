# assignments.py
from telebot import types
from sqlmodel import Session, select
from models import Assignment, User
from database import engine
from utils import is_admin, get_or_create_user
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from texts import (
    ARABIC_DAY_NAMES, ASSIGNMENTS_MENU, VIEW_UPCOMING_ASSIGNMENTS, CREATE_NEW_ASSIGNMENT,
    NO_UPCOMING_ASSIGNMENTS, ASSIGNMENT_INFO, NO_ASSIGNMENT_PERMISSION,
    ENTER_ASSIGNMENT_TITLE, ENTER_ASSIGNMENT_DESCRIPTION,
    ENTER_ASSIGNMENT_DUE_DATE, SEND_ASSIGNMENT_FILE,
    INVALID_DATE_FORMAT, INVALID_INPUT_ASSIGNMENT_SAVED,
    ASSIGNMENT_CREATED_SUCCESSFULLY, USER_NOT_FOUND_ERROR,
    EDIT_ASSIGNMENT, DELETE_ASSIGNMENT, SELECT_ASSIGNMENT_TO_EDIT,
    SELECT_ASSIGNMENT_TO_DELETE, NO_ASSIGNMENTS_TO_EDIT,
    NO_ASSIGNMENTS_TO_DELETE, ENTER_NEW_ASSIGNMENT_TITLE,
    ENTER_NEW_ASSIGNMENT_DESCRIPTION, ENTER_NEW_ASSIGNMENT_DUE_DATE,
    ASSIGNMENT_UPDATED_SUCCESSFULLY, CONFIRM_ASSIGNMENT_DELETE,
    ASSIGNMENT_DELETED_SUCCESSFULLY, ASSIGNMENT_DELETION_CANCELLED
)

def assignments_menu(message, send_message_once):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton(VIEW_UPCOMING_ASSIGNMENTS, callback_data="view_assignments"))
    if is_admin(message.from_user.id):
        keyboard.row(types.InlineKeyboardButton(CREATE_NEW_ASSIGNMENT, callback_data="create_assignment"))
        keyboard.row(types.InlineKeyboardButton(EDIT_ASSIGNMENT, callback_data="edit_assignment"))
        keyboard.row(types.InlineKeyboardButton(DELETE_ASSIGNMENT, callback_data="delete_assignment"))
    send_message_once(message.chat.id, ASSIGNMENTS_MENU, reply_markup=keyboard)


def view_assignments(call, send_message_once):
    now = datetime.now()
    days_until_next_thursday = (3 - now.weekday() + 7) % 7 + 7
    end_of_next_week = now + timedelta(days=days_until_next_thursday)
    
    with Session(engine) as session:
        assignments = session.exec(
            select(Assignment)
            .where(Assignment.due_date >= now)
            .where(Assignment.due_date <= end_of_next_week)
            .order_by(Assignment.due_date)
        ).all()
    
    if not assignments:
        send_message_once(call.message.chat.id, NO_UPCOMING_ASSIGNMENTS)
        return

    for assignment in assignments:
        arabic_day_name = ARABIC_DAY_NAMES[assignment.due_date.weekday()]
        formatted_date = assignment.due_date.strftime('%m/%d')
        assignment_text = ASSIGNMENT_INFO.format(
            title=assignment.title,
            due_date=f"{arabic_day_name} {formatted_date}",
            description=assignment.description
        )
        
        if assignment.file_id:
            send_message_once(call.message.chat.id, assignment_text, document=assignment.file_id)
        else:
            send_message_once(call.message.chat.id, assignment_text)

def create_assignment_prompt(call, send_message_once):
    if not is_admin(call.from_user.id):
        send_message_once(call.message.chat.id, NO_ASSIGNMENT_PERMISSION)
        return
    
    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_id == call.from_user.id)).first()
        if not user:
            user = User(telegram_id=call.from_user.id)
            session.add(user)
        user.assignment_state = 'waiting_for_title'
        user.lecture_state = None  # Clear lecture state
        session.commit()
    
    send_message_once(call.message.chat.id, ENTER_ASSIGNMENT_TITLE)

def handle_assignment_steps(message, send_message_once):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_id == message.from_user.id)).first()
        if not user or not user.assignment_state:
            return False

        if user.assignment_state == 'waiting_for_title':
            return process_assignment_title(message, user.telegram_id, send_message_once)
        elif user.assignment_state == 'waiting_for_description':
            return process_assignment_description(message, user.telegram_id, send_message_once)
        elif user.assignment_state == 'waiting_for_due_date':
            return process_assignment_due_date(message, user.telegram_id, send_message_once)
        elif user.assignment_state == 'waiting_for_file':
            return save_assignment(message, user.telegram_id, send_message_once)
        
        return False

def process_assignment_title(message, telegram_id, send_message_once):
    title = message.text
    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_id == telegram_id)).first()
        if user:
            user.assignment_title = title
            user.assignment_state = 'waiting_for_description'
            session.commit()
            send_message_once(message.chat.id, ENTER_ASSIGNMENT_DESCRIPTION)
        else:
            send_message_once(message.chat.id, USER_NOT_FOUND_ERROR)

def process_assignment_description(message, telegram_id, send_message_once):
    description = message.text
    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_id == telegram_id)).first()
        if user:
            user.assignment_description = description
            user.assignment_state = 'waiting_for_due_date'
            session.commit()
            send_message_once(message.chat.id, ENTER_ASSIGNMENT_DUE_DATE)
        else:
            send_message_once(message.chat.id, USER_NOT_FOUND_ERROR)

def process_assignment_due_date(message, telegram_id, send_message_once):
    try:
        date_input = message.text.strip()
        add_week = False
        if date_input.endswith('+7'):
            add_week = True
            date_input = date_input[:-2]  # Remove the '+7'

        due_date = datetime.strptime(f"{datetime.now().year}-{date_input}", "%Y-%m-%d")
        
        if add_week:
            due_date += timedelta(days=7)

        if due_date < datetime.now():
            due_date = due_date.replace(year=due_date.year + 1)

        with Session(engine) as session:
            user = session.exec(select(User).where(User.telegram_id == telegram_id)).first()
            if user:
                user.assignment_due_date = due_date
                user.assignment_state = 'waiting_for_file'
                session.commit()
                
                arabic_day_name = ARABIC_DAY_NAMES[due_date.weekday()]
                formatted_date = due_date.strftime('%m/%d')
                confirmation_message = f"تم تعيين تاريخ الاستحقاق: {arabic_day_name} {formatted_date}"
                send_message_once(message.chat.id, confirmation_message)
                send_message_once(message.chat.id, SEND_ASSIGNMENT_FILE)
            else:
                send_message_once(message.chat.id, USER_NOT_FOUND_ERROR)
    except ValueError:
        send_message_once(message.chat.id, INVALID_DATE_FORMAT)

def save_assignment(message, telegram_id, send_message_once):
    file_id = None
    if message.document:
        file_id = message.document.file_id
    elif message.text != "/skip":
        send_message_once(message.chat.id, INVALID_INPUT_ASSIGNMENT_SAVED)

    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_id == telegram_id)).first()
        if not user:
            send_message_once(message.chat.id, USER_NOT_FOUND_ERROR)
            return

        assignment = Assignment(
            title=user.assignment_title,
            description=user.assignment_description,
            due_date=user.assignment_due_date,
            file_id=file_id
        )
        session.add(assignment)
        
        # Clear the user's assignment-related fields
        user.assignment_state = None
        user.assignment_title = None
        user.assignment_description = None
        user.assignment_due_date = None
        
        session.commit()
        
        # Refresh the assignment object to ensure all attributes are loaded
        session.refresh(assignment)
        
        # Format the message within the session
        success_message = ASSIGNMENT_CREATED_SUCCESSFULLY.format(
            title=assignment.title,
            due_date=assignment.due_date.strftime('%a, %b %d')
        )
    
    # Send the message outside the session
    send_message_once(message.chat.id, success_message)

def edit_assignment_prompt(call, send_message_once):
    if not is_admin(call.from_user.id):
        send_message_once(call.message.chat.id, NO_ASSIGNMENT_PERMISSION)
        return

    with Session(engine) as session:
        assignments = session.exec(select(Assignment).order_by(Assignment.due_date)).all()

    if not assignments:
        send_message_once(call.message.chat.id, NO_ASSIGNMENTS_TO_EDIT)
        return

    keyboard = types.InlineKeyboardMarkup()
    for assignment in assignments:
        button_text = f"{assignment.title} (Due: {assignment.due_date.strftime('%Y-%m-%d')})"
        keyboard.add(types.InlineKeyboardButton(button_text, callback_data=f"edit_assignment_{assignment.id}"))
    
    send_message_once(call.message.chat.id, SELECT_ASSIGNMENT_TO_EDIT, reply_markup=keyboard)

def edit_assignment(call, send_message_once):
    assignment_id = int(call.data.split("_")[-1])
    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_id == call.from_user.id)).first()
        if not user:
            user = User(telegram_id=call.from_user.id)
            session.add(user)
        user.assignment_state = 'editing_title'
        user.temp_assignment_id = assignment_id
        session.commit()
    
    send_message_once(call.message.chat.id, ENTER_NEW_ASSIGNMENT_TITLE)

def handle_edit_assignment_steps(message, send_message_once):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_id == message.from_user.id)).first()
        if not user or not user.assignment_state or not user.assignment_state.startswith('editing_'):
            return False

        assignment = session.get(Assignment, user.temp_assignment_id)
        if not assignment:
            send_message_once(message.chat.id, USER_NOT_FOUND_ERROR)
            return True

        if user.assignment_state == 'editing_title':
            assignment.title = message.text
            user.assignment_state = 'editing_description'
            session.commit()
            send_message_once(message.chat.id, ENTER_NEW_ASSIGNMENT_DESCRIPTION)
        elif user.assignment_state == 'editing_description':
            assignment.description = message.text
            user.assignment_state = 'editing_due_date'
            session.commit()
            send_message_once(message.chat.id, ENTER_NEW_ASSIGNMENT_DUE_DATE)
        elif user.assignment_state == 'editing_due_date':
            try:
                due_date = process_due_date(message.text)
                assignment.due_date = due_date
                user.assignment_state = None
                user.temp_assignment_id = None
                session.commit()
                send_message_once(message.chat.id, ASSIGNMENT_UPDATED_SUCCESSFULLY)
            except ValueError:
                send_message_once(message.chat.id, INVALID_DATE_FORMAT)
        
        return True

def delete_assignment_prompt(call, send_message_once):
    if not is_admin(call.from_user.id):
        send_message_once(call.message.chat.id, NO_ASSIGNMENT_PERMISSION)
        return

    with Session(engine) as session:
        assignments = session.exec(select(Assignment).order_by(Assignment.due_date)).all()

    if not assignments:
        send_message_once(call.message.chat.id, NO_ASSIGNMENTS_TO_DELETE)
        return

    keyboard = types.InlineKeyboardMarkup()
    for assignment in assignments:
        button_text = f"{assignment.title} (Due: {assignment.due_date.strftime('%Y-%m-%d')})"
        keyboard.add(types.InlineKeyboardButton(button_text, callback_data=f"delete_assignment_{assignment.id}"))
    
    send_message_once(call.message.chat.id, SELECT_ASSIGNMENT_TO_DELETE, reply_markup=keyboard)

def delete_assignment_confirm(call, send_message_once):
    assignment_id = int(call.data.split("_")[-1])
    with Session(engine) as session:
        assignment = session.get(Assignment, assignment_id)
        if assignment:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(
                types.InlineKeyboardButton("نعم", callback_data=f"confirm_delete_assignment_{assignment_id}"),
                types.InlineKeyboardButton("لا", callback_data="cancel_delete_assignment")
            )
            confirm_message = CONFIRM_ASSIGNMENT_DELETE.format(
                title=assignment.title,
                due_date=assignment.due_date.strftime('%Y-%m-%d')
            )
            send_message_once(call.message.chat.id, confirm_message, reply_markup=keyboard)
        else:
            send_message_once(call.message.chat.id, USER_NOT_FOUND_ERROR)

def delete_assignment(call, send_message_once):
    assignment_id = int(call.data.split("_")[-1])
    with Session(engine) as session:
        assignment = session.get(Assignment, assignment_id)
        if assignment:
            session.delete(assignment)
            session.commit()
            success_message = ASSIGNMENT_DELETED_SUCCESSFULLY.format(
                title=assignment.title,
                due_date=assignment.due_date.strftime('%Y-%m-%d')
            )
            send_message_once(call.message.chat.id, success_message)
        else:
            send_message_once(call.message.chat.id, USER_NOT_FOUND_ERROR)

def cancel_delete_assignment(call, send_message_once):
    send_message_once(call.message.chat.id, ASSIGNMENT_DELETION_CANCELLED)

def process_due_date(date_input):
    date_input = date_input.strip()
    add_week = False
    if date_input.endswith('+7'):
        add_week = True
        date_input = date_input[:-2]  # Remove the '+7'

    due_date = datetime.strptime(f"{datetime.now().year}-{date_input}", "%Y-%m-%d")
    
    if add_week:
        due_date += timedelta(days=7)

    if due_date < datetime.now():
        due_date = due_date.replace(year=due_date.year + 1)

    return due_date