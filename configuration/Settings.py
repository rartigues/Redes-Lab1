from ast import Raise
import logging
import os
import traceback
from dotenv import load_dotenv

load_dotenv()

class Settings:
    try:
        IP = os.getenv("IP")
        PORT = int(os.getenv("PORT"))
        ADDR = (IP, PORT)
        FORMAT = "utf-8"
    except Exception as e:
        print("\n!!!!!!!!!Error: .env missing!!!!!!!!!")
        raise e