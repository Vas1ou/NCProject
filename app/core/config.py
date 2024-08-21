from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Nord Clan Project"
    DATABASE_URL: str = "postgresql+asyncpg://myuser:mypassword@localhost/mydatabase"

settings = Settings()
