from sqlmodel import SQLModel, create_engine
import os
from config import DATABASE_URL


engine = create_engine(DATABASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)