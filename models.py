from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(unique=True, index=True)
    username: str
    is_admin: bool = Field(default=False)
    awaiting_task: Optional[str] = None

class Assignment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    due_date: datetime
    is_homework: bool
    photo_id: Optional[str] = None