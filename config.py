import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_HOST     = os.getenv('DB_HOST', 'localhost')
    DB_USER     = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME     = os.getenv('DB_NAME', 'resume_screener')
    REDIS_URL   = os.getenv('REDIS_URL', 'redis://localhost:6379')
    SECRET_KEY  = os.getenv('SECRET_KEY', 'dev')
