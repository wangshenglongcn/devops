from dotenv import load_dotenv
import os

load_dotenv()  # 从 .env 读
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
}
