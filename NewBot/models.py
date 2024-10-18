from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    telegram_id: int = Field(unique=True, index=True)
    is_admin: bool = Field(default=False)
    # Fields for lecture creation
    temp_subject_id: Optional[int] = None
    temp_lecture_number: Optional[int] = None
    temp_lecture_title: Optional[str] = None
    lecture_state: Optional[str] = None
    # Fields for assignment creation
    assignment_state: Optional[str] = None
    assignment_title: Optional[str] = None
    assignment_description: Optional[str] = None
    assignment_due_date: Optional[datetime] = None

    temp_assignment_id: Optional[int] = None

    photo_ids: Optional[str] = None

class Subject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    lectures: List["Lecture"] = Relationship(back_populates="subject")

class Lecture(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    subject_id: int = Field(foreign_key="subject.id")
    subject: Subject = Relationship(back_populates="lectures")
    lecture_number: int
    title: str
    file_id: str

class Assignment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    file_id: Optional[str] = None
    due_date: datetime