from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlmodel import Session, select
from models import User, Assignment
from utils import get_or_create_user, translate_day_name
from config import ADMIN_PASSWORD, DATABASE_URL, GROUP_CHAT_ID
from datetime import datetime, timedelta
import logging
from sqlmodel import create_engine

engine = create_engine(DATABASE_URL)

# Handler for the /start command
@Client.on_message(filters.command("start"))
async def start_command(client, message):
    try:
        user = get_or_create_user(message.from_user.id, message.from_user.username or "")
        if user.is_admin:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("إضافة واجب", callback_data="add_homework"),
                 InlineKeyboardButton("إضافة مهمة", callback_data="add_assignment")],
                [InlineKeyboardButton("عرض الأسبوع القادم", callback_data="view_next_week")],
                [InlineKeyboardButton("تعديل مهمة", callback_data="edit_assignment"),
                 InlineKeyboardButton("حذف مهمة", callback_data="delete_assignment")],
                [InlineKeyboardButton("تعديل واجب", callback_data="edit_homework"),
                 InlineKeyboardButton("حذف واجب", callback_data="delete_homework")]
            ])
            await message.reply_text("مرحبًا ، أي شيء تريد القيام به؟", reply_markup=keyboard)
        else:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("عرض الأسبوع القادم", callback_data="view_next_week")]
            ])
            await message.reply_text("مرحبًا! إليك ما يمكنك فعله:", reply_markup=keyboard)
    except Exception as e:
        logging.error(f"Error in start_command: {e}")
        await message.reply_text("حدث خطأ. يرجى المحاولة مرة أخرى لاحقًا.")

# Handler for adding homework/assignment
@Client.on_callback_query(filters.regex('^add_(homework|assignment)$'))
async def add_task(client, callback_query):
    user = get_or_create_user(callback_query.from_user.id, callback_query.from_user.username or "")
    if not user.is_admin:
        await callback_query.answer("ليس لديك إذن لإضافة مهام.", show_alert=True)
        return

    task_type = "واجب" if callback_query.data == "add_homework" else "مهمة"
    await callback_query.message.reply_text(f"الرجاء إدخال تفاصيل {task_type} بالتنسيق التالي:\n"
                                            f"العنوان | الوصف | تاريخ الاستحقاق (YYYY-MM-DD)\n"
                                            f"يمكنك أيضًا إرفاق صورة مع التفاصيل في التعليق.")
    
    user.awaiting_task = task_type
    with Session(engine) as session:
        session.add(user)
        session.commit()

# Handler for receiving task details (text or photo)
@Client.on_message((filters.text | filters.photo) & ~filters.command("start") & ~filters.command("make_admin") & ~filters.command("become_admin"))
async def receive_task_details(client, message):
    user = get_or_create_user(message.from_user.id, message.from_user.username or "")
    if not hasattr(user, 'awaiting_task') or user.awaiting_task is None:
        return

    try:
        if message.photo:
            if not message.caption:
                await message.reply_text("الرجاء إرفاق التفاصيل في تعليق الصورة.")
                return
            details = message.caption.strip()
            photo_id = message.photo.file_id
        else:
            details = message.text.strip()
            photo_id = None

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

        await message.reply_text(f"{user.awaiting_task} تمت إضافته بنجاح!")
    except Exception as e:
        await message.reply_text(f"خطأ في إضافة {user.awaiting_task.lower()}. يرجى التحقق من التنسيق والمحاولة مرة أخرى.")
    finally:
        user.awaiting_task = None
        with Session(engine) as session:
            session.add(user)
            session.commit()

# Handler for viewing next week's tasks
@Client.on_callback_query(filters.regex('^view_next_week$'))
async def view_next_week(client, callback_query):
    await send_next_week_tasks(client, callback_query.message.chat.id, is_admin=callback_query.from_user.is_admin)

# Function to send next week's tasks
async def send_next_week_tasks(client, chat_id, is_admin=False):
    today = datetime.now().date()
    next_week_start = today + timedelta(days=(6 - today.weekday()))  # Start from Sunday
    next_week_end = next_week_start + timedelta(days=4)  # End on Thursday

    with Session(engine) as session:
        tasks = session.exec(select(Assignment).where(
            Assignment.due_date.between(next_week_start, next_week_end)
        ).order_by(Assignment.due_date)).all()

    if not tasks:
        await client.send_message(chat_id, "لا توجد مهام للأسبوع القادم!")
        return

    tasks_by_day = {}
    for task in tasks:
        day = task.due_date.strftime('%Y-%m-%d')
        if day not in tasks_by_day:
            tasks_by_day[day] = []
        tasks_by_day[day].append(task)

    for day, day_tasks in tasks_by_day.items():
        message = f"مهام يوم {translate_day_name(datetime.strptime(day, '%Y-%m-%d').strftime('%A'))} ({day}):\n\n"
        for task in day_tasks:
            task_type = "واجب" if task.is_homework else "مهمة"
            message += f"{task_type}: {task.title}\n"
            message += f"الوصف: {task.description}\n"
            if task.photo_id:
                message += "(تحتوي على صورة)\n"
            message += "\n"

            if is_admin:
                edit_button = InlineKeyboardButton(f"تعديل {task_type}", callback_data=f"edit_{'homework' if task.is_homework else 'assignment'}_{task.id}")
                delete_button = InlineKeyboardButton(f"حذف {task_type}", callback_data=f"delete_{'homework' if task.is_homework else 'assignment'}_{task.id}")
                keyboard = InlineKeyboardMarkup([[edit_button, delete_button]])
                await client.send_message(chat_id, message, reply_markup=keyboard)
            else:
                await client.send_message(chat_id, message)

            if task.photo_id:
                await client.send_photo(chat_id, task.photo_id)

# Handler for editing task
@Client.on_callback_query(filters.regex('^edit_(homework|assignment)_(\d+)$'))
async def edit_task(client, callback_query):
    user = get_or_create_user(callback_query.from_user.id, callback_query.from_user.username or "")
    if not user.is_admin:
        await callback_query.answer("ليس لديك إذن لتعديل المهام.", show_alert=True)
        return

    task_type = "واجب" if callback_query.data.startswith("edit_homework") else "مهمة"
    task_id = int(callback_query.data.split('_')[-1])

    with Session(engine) as session:
        task = session.get(Assignment, task_id)
        if not task:
            await callback_query.answer("المهمة غير موجودة.", show_alert=True)
            return

        await callback_query.message.reply_text(f"الرجاء إدخال تفاصيل {task_type} الجديدة بالتنسيق التالي:\n"
                                                f"العنوان | الوصف | تاريخ الاستحقاق (YYYY-MM-DD)\n"
                                                f"يمكنك أيضًا إرفاق صورة جديدة مع التفاصيل في التعليق.")
        
        user.awaiting_task = f"edit_{task_type}_{task_id}"
        session.add(user)
        session.commit()

# Handler for deleting task
@Client.on_callback_query(filters.regex('^delete_(homework|assignment)_(\d+)$'))
async def delete_task(client, callback_query):
    user = get_or_create_user(callback_query.from_user.id, callback_query.from_user.username or "")
    if not user.is_admin:
        await callback_query.answer("ليس لديك إذن لحذف المهام.", show_alert=True)
        return

    task_type = "واجب" if callback_query.data.startswith("delete_homework") else "مهمة"
    task_id = int(callback_query.data.split('_')[-1])

    with Session(engine) as session:
        task = session.get(Assignment, task_id)
        if not task:
            await callback_query.answer("المهمة غير موجودة.", show_alert=True)
            return

        session.delete(task)
        session.commit()

    await callback_query.answer(f"{task_type} تم حذفه بنجاح!", show_alert=True)
    await send_next_week_tasks(client, callback_query.message.chat.id, is_admin=user.is_admin)

# Function to send daily updates
async def send_daily_update(client):
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
        message += f"{task_type}: {task.title}\n"
        message += f"الوصف: {task.description}\n"
        if task.photo_id:
            message += "(تحتوي على صورة)\n"
        message += "\n"

    await client.send_message(GROUP_CHAT_ID, message)

    for task in tasks:
        if task.photo_id:
            await client.send_photo(GROUP_CHAT_ID, task.photo_id)

# Handler for the /make_admin command (only for existing admins)
@Client.on_message(filters.command("make_admin"))
async def make_admin(client, message):
    try:
        user = get_or_create_user(message.from_user.id, message.from_user.username or "")
        if user.is_admin:
            if message.reply_to_message:
                target_user_id = message.reply_to_message.from_user.id
                target_username = message.reply_to_message.from_user.username or ""
                with Session(engine) as session:
                    target_user = get_or_create_user(target_user_id, target_username)
                    target_user.is_admin = True
                    session.add(target_user)
                    session.commit()
                await message.reply_text(f"المستخدم {target_username} أصبح الآن مشرفًا.")
            else:
                await message.reply_text("يرجى الرد على رسالة المستخدم لجعله مشرفًا.")
        else:
            await message.reply_text("عذرًا، فقط المشرفون يمكنهم استخدام هذا الأمر.")
    except Exception as e:
        logging.error(f"Error in make_admin: {e}")
        await message.reply_text("حدث خطأ. يرجى المحاولة مرة أخرى لاحقًا.")

# Handler for the /become_admin command
@Client.on_message(filters.command("become_admin"))
async def become_admin(client, message):
    try:
        command_args = message.text.split()
        if len(command_args) < 2:
            await message.reply_text("يرجى تقديم كلمة مرور المشرف.")
            return

        provided_password = command_args[1]

        if provided_password == ADMIN_PASSWORD:
            user = get_or_create_user(message.from_user.id, message.from_user.username or "")
            user.is_admin = True
            with Session(engine) as session:
                session.add(user)
                session.commit()
            await message.reply_text("تهانينا! أنت الآن مشرف.")
        else:
            await message.reply_text("كلمة المرور غير صحيحة. لا يمكنك أن تصبح مشرفًا.")
    except Exception as e:
        logging.error(f"Error in become_admin: {e}")
        await message.reply_text("حدث خطأ. يرجى المحاولة مرة أخرى لاحقًا.")

@Client.on_message(filters.group)
async def get_group_id(client, message):
    print(f"Group ID: {message.chat.id}")
    await message.reply(f"This group's ID is: {message.chat.id}")