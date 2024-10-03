from sqlmodel import Session, select
from models import User
from config import DATABASE_URL
from sqlmodel import create_engine

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