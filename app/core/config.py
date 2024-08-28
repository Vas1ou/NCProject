from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Загружаем переменные из .env файла
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")


class Settings(BaseSettings):
    PROJECT_NAME: str = "Nord Clan Project"
    DATABASE_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


settings = Settings()
