from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlmodel import Session, select, create_engine
from models import User, Assignment
from utils import get_or_create_user, translate_day_name, handle_error
from config import ADMIN_PASSWORD, DATABASE_URL, API_ID, API_HASH, BOT_TOKEN ,GROUP_CHAT_ID
from datetime import datetime, timedelta
import logging
from text_constants import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
engine = create_engine(DATABASE_URL)

def is_admin(user_id: int) -> bool:
    with Session(engine) as session:
        user = session.exec(select(User).where(User.user_id == user_id)).first()
        return user.is_admin if user else False

async def send_message_with_error_handling(chat_id: int, text: str, reply_markup=None):
    try:
        await app.send_message(chat_id, text, reply_markup=reply_markup)
    except Exception as e:
        await handle_error(app, "send_message", e, chat_id)

@app.on_message(filters.command("start"))
async def start_command(_, message):
    try:
        user = get_or_create_user(message.from_user.id, message.from_user.username or "")
        keyboard = InlineKeyboardMarkup(ADMIN_KEYBOARD if user.is_admin else USER_KEYBOARD)
        text = START_MESSAGE if user.is_admin else USER_START_MESSAGE
        await send_message_with_error_handling(message.chat.id, text, keyboard)
    except Exception as e:
        await handle_error(app, "start_command", e, message.chat.id)

@app.on_message(filters.command("make_admin"))
async def make_admin(_, message):
    if not is_admin(message.from_user.id):
        await send_message_with_error_handling(message.chat.id, ADMIN_ONLY_COMMAND)
        return

    if not message.reply_to_message:
        await send_message_with_error_handling(message.chat.id, MAKE_ADMIN_REPLY_REQUIRED)
        return

    try:
        target_user_id = message.reply_to_message.from_user.id
        target_username = message.reply_to_message.from_user.username or ""
        with Session(engine) as session:
            target_user = get_or_create_user(target_user_id, target_username)
            target_user.is_admin = True
            session.add(target_user)
            session.commit()
        await send_message_with_error_handling(message.chat.id, MAKE_ADMIN_SUCCESS.format(target_username=target_username))
    except Exception as e:
        await handle_error(app, "make_admin", e, message.chat.id)

@app.on_message(filters.command("become_admin"))
async def become_admin(_, message):
    try:
        command_args = message.text.split()
        if len(command_args) < 2:
            await send_message_with_error_handling(message.chat.id, PROVIDE_ADMIN_PASSWORD)
            return

        provided_password = command_args[1]

        if provided_password == ADMIN_PASSWORD:
            user = get_or_create_user(message.from_user.id, message.from_user.username or "")
            user.is_admin = True
            with Session(engine) as session:
                session.add(user)
                session.commit()
            await send_message_with_error_handling(message.chat.id, ADMIN_PASSWORD_SUCCESS)
        else:
            await send_message_with_error_handling(message.chat.id, ADMIN_PASSWORD_FAIL)
    except Exception as e:
        await handle_error(app, "become_admin", e, message.chat.id)

@app.on_callback_query(filters.regex('^add_(homework|assignment)$'))
async def add_task(_, callback_query):
    if not is_admin(callback_query.from_user.id):
        await callback_query.answer(NO_PERMISSION_MESSAGE, show_alert=True)
        return

    task_type = "واجب" if callback_query.data == "add_homework" else "مهمة"
    await send_message_with_error_handling(callback_query.message.chat.id, ADD_TASK_INSTRUCTIONS.format(task_type=task_type))
    
    with Session(engine) as session:
        user = session.exec(select(User).where(User.user_id == callback_query.from_user.id)).one()
        user.awaiting_task = task_type
        session.add(user)
        session.commit()

@app.on_callback_query(filters.regex('^view_next_week$'))
async def view_next_week(_, callback_query):
    user_is_admin = is_admin(callback_query.from_user.id)
    await send_next_week_tasks(callback_query.message.chat.id, user_is_admin)

@app.on_callback_query(filters.regex('^(edit|delete)_(homework|assignment)_(\d+)$'))
async def handle_task_action(_, callback_query):
    if not is_admin(callback_query.from_user.id):
        await callback_query.answer(NO_PERMISSION_DELETE, show_alert=True)
        return

    action, task_type, task_id = callback_query.data.split('_')
    task_id = int(task_id)

    with Session(engine) as session:
        task = session.get(Assignment, task_id)
        if not task:
            await callback_query.answer(TASK_NOT_EXIST, show_alert=True)
            return

        if action == 'edit':
            await send_message_with_error_handling(callback_query.message.chat.id, EDIT_TASK_INSTRUCTIONS.format(task_type=task_type))
            user = session.exec(select(User).where(User.user_id == callback_query.from_user.id)).one()
            user.awaiting_task = f"edit_{task_type}_{task_id}"
            session.add(user)
            session.commit()
        else:  # delete
            session.delete(task)
            session.commit()
            await callback_query.answer(TASK_DELETED_SUCCESS.format(task_type=task_type), show_alert=True)
            await send_next_week_tasks(callback_query.message.chat.id, is_admin=True)

@app.on_message(filters.text | filters.photo)
async def handle_message(_, message):
    user = get_or_create_user(message.from_user.id, message.from_user.username or "")
    if user.awaiting_task:
        if user.awaiting_task.startswith("edit_"):
            await handle_edit_task(message, user)
        else:
            await handle_add_task(message, user)
    else:
        await send_message_with_error_handling(message.chat.id, DEFAULT_RESPONSE)

async def handle_add_task(message, user):
    try:
        details, photo_id = get_task_details(message)
        title, description, due_date_str = [part.strip() for part in details.split('|')]
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        
        with Session(engine) as session:
            new_task = Assignment(
                title=title,
                description=description,
                due_date=due_date,
                is_homework=(user.awaiting_task == "واجب"),
                photo_id=photo_id
            )
            session.add(new_task)
            session.commit()

        await send_message_with_error_handling(message.chat.id, TASK_ADDED_SUCCESS.format(task_type=user.awaiting_task))
    except Exception as e:
        await send_message_with_error_handling(message.chat.id, f"خطأ في إضافة {user.awaiting_task.lower()}. يرجى التحقق من التنسيق والمحاولة مرة أخرى.")
    finally:
        clear_awaiting_task(user)

async def handle_edit_task(message, user):
    _, task_type, task_id = user.awaiting_task.split("_")
    try:
        details, photo_id = get_task_details(message)
        title, description, due_date_str = [part.strip() for part in details.split('|')]
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        
        with Session(engine) as session:
            task = session.get(Assignment, int(task_id))
            if task:
                task.title = title
                task.description = description
                task.due_date = due_date
                if photo_id:
                    task.photo_id = photo_id
                session.add(task)
                session.commit()
                await send_message_with_error_handling(message.chat.id, TASK_UPDATED_SUCCESS.format(task_type=task_type))
            else:
                await send_message_with_error_handling(message.chat.id, TASK_NOT_EXIST)
    except Exception as e:
        await send_message_with_error_handling(message.chat.id, f"خطأ في تحديث {task_type}. يرجى التحقق من التنسيق والمحاولة مرة أخرى.")
    finally:
        clear_awaiting_task(user)

def get_task_details(message):
    if message.photo:
        if not message.caption:
            raise ValueError(MISSING_CAPTION)
        return message.caption.strip(), message.photo.file_id
    return message.text.strip(), None

def clear_awaiting_task(user):
    with Session(engine) as session:
        user.awaiting_task = None
        session.add(user)
        session.commit()

async def send_next_week_tasks(chat_id, is_admin=False):
    today = datetime.now().date()
    
    # Adjust for Sunday-Thursday week
    days_until_sunday = (6 - today.weekday()) % 7
    this_week_start = today - timedelta(days=today.weekday())
    next_week_start = this_week_start + timedelta(days=7)
    
    this_week_end = this_week_start + timedelta(days=4)  # Thursday
    next_week_end = next_week_start + timedelta(days=4)  # Next Thursday

    with Session(engine) as session:
        tasks = session.exec(select(Assignment).where(
            (Assignment.due_date.between(today, this_week_end) & Assignment.is_homework) |
            (Assignment.due_date.between(next_week_start, next_week_end))
        ).order_by(Assignment.due_date)).all()

    if not tasks:
        await send_message_with_error_handling(chat_id, NO_TASKS_NEXT_WEEK)
        return

    for task in tasks:
        task_date = task.due_date.date() if isinstance(task.due_date, datetime) else task.due_date
        day = task_date.strftime('%Y-%m-%d')
        day_name = translate_day_name(task_date.strftime('%A'))
        task_type = "واجب" if task.is_homework else "مهمة"
        week_indicator = "هذا الأسبوع" if task_date < next_week_start else "الأسبوع القادم"
        message = f"{day_name} ({day}) - {week_indicator}:\n"
        message += f"{task_type}: {task.title}\n"
        message += f"الوصف: {task.description}\n"

        if task.photo_id:
            if is_admin:
                edit_button = InlineKeyboardButton(f"تعديل {task_type}", callback_data=f"edit_{'homework' if task.is_homework else 'assignment'}_{task.id}")
                delete_button = InlineKeyboardButton(f"حذف {task_type}", callback_data=f"delete_{'homework' if task.is_homework else 'assignment'}_{task.id}")
                keyboard = InlineKeyboardMarkup([[edit_button, delete_button]])
                await app.send_photo(chat_id, task.photo_id, caption=message, reply_markup=keyboard)
            else:
                await app.send_photo(chat_id, task.photo_id, caption=message)
        else:
            if is_admin:
                edit_button = InlineKeyboardButton(f"تعديل {task_type}", callback_data=f"edit_{'homework' if task.is_homework else 'assignment'}_{task.id}")
                delete_button = InlineKeyboardButton(f"حذف {task_type}", callback_data=f"delete_{'homework' if task.is_homework else 'assignment'}_{task.id}")
                keyboard = InlineKeyboardMarkup([[edit_button, delete_button]])
                await send_message_with_error_handling(chat_id, message, keyboard)
            else:
                await send_message_with_error_handling(chat_id, message)

async def send_daily_update():
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    with Session(engine) as session:
        tasks = session.exec(select(Assignment).where(
            Assignment.due_date.between(today, tomorrow)
        ).order_by(Assignment.due_date)).all()

    if not tasks:
        return

    message = f"مهام اليوم ({today.strftime('%Y-%m-%d')}):\n\n"
    for task in tasks:
        task_type = "واجب" if task.is_homework else "مهمة"
        task_message = f"{task_type}: {task.title}\n"
        task_message += f"الوصف: {task.description}\n"

        if task.photo_id:
            task_message += "(تحتوي على صورة)\n"
            await app.send_photo(GROUP_CHAT_ID, task.photo_id, caption=task_message)
        else:
            await send_message_with_error_handling(GROUP_CHAT_ID, task_message)

    with Session(engine) as session:
        admin_users = session.exec(select(User).where(User.is_admin == True)).all()
        for admin_user in admin_users:
            try:
                for task in tasks:
                    task_type = "واجب" if task.is_homework else "مهمة"
                    task_message = f"{task_type}: {task.title}\n"
                    task_message += f"الوصف: {task.description}\n"

                    if task.photo_id:
                        task_message += "(تحتوي على صورة)\n"
                        await app.send_photo(admin_user.user_id, task.photo_id, caption=task_message)
                    else:
                        await send_message_with_error_handling(admin_user.user_id, task_message)
            except Exception as e:
                logger.error(f"Failed to send daily update to admin {admin_user.user_id}: {str(e)}")

@app.on_message(filters.command("send_daily_update"))
async def manual_send_daily_update(_, message):
    if is_admin(message.from_user.id):
        await send_daily_update()
        await send_message_with_error_handling(message.chat.id, "Daily update sent to all admin users.")
    else:
        await send_message_with_error_handling(message.chat.id, ADMIN_ONLY_COMMAND)