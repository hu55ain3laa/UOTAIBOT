from sqlmodel import Session, select
from models import User
from config import DATABASE_URL
from sqlmodel import create_engine
import logging
from pyrogram import Client
from config import GROUP_CHAT_ID

engine = create_engine(DATABASE_URL)

def get_or_create_user(user_id: int, username: str) -> User:
    with Session(engine) as session:
        user = session.exec(select(User).where(User.user_id == user_id)).first()
        if user is None:
            user = User(user_id=user_id, username=username)
            session.add(user)
            session.commit()
            session.refresh(user)
        return user

def translate_day_name(day_name):
    day_translations = {
        "Sunday": "الأحد",
        "Monday": "الاثنين",
        "Tuesday": "الثلاثاء",
        "Wednesday": "الأربعاء",
        "Thursday": "الخميس",
        "Friday": "الجمعة",
        "Saturday": "السبت"
    }
    return day_translations.get(day_name, day_name)

logger = logging.getLogger(__name__)

async def handle_error(app: Client, context: str, error: Exception, chat_id: int = None):
    error_message = f"Error in {context}: {str(error)}"
    logger.error(error_message)
    
    if chat_id:
        await app.send_message(chat_id, "حدث خطأ. يرجى المحاولة مرة أخرى لاحقًا.")
    
    # Optionally, send error to admin group
    await app.send_message(GROUP_CHAT_ID, f"Admin Alert: {error_message}")