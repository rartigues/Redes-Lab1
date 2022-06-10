import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    IP = os.getenv("IP")
    PORT = int(os.getenv("PORT"))
    ADDR = (IP, PORT)
    FORMAT = "utf-8"