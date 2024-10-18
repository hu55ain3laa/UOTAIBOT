# config.py
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = f"mysql+pymysql://avnadmin:AVNS_2QjoUe49JiWOaAc3_Pt@mysql84-unique.h.aivencloud.com:23839/defaultdb?"
USE_GPU = os.getenv("USE_GPU", "False").lower() == "true"