import os
import secrets

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    
    PROJECT_NAME: str = 'Kebab API'

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days

    SQLALCHEMY_DATABASE_URI: str = os.environ.get('SQLALCHEMY_DATABASE_URI')
    # SQLALCHEMY_DATABASE_URI: str = "sqlite:///./app.db"e

    FIRST_SUPERUSER: str = os.environ.get('FIRST_SUPERUSER')
    FIRST_SUPERUSER_PASSWORD: str = os.environ.get('FIRST_SUPERUSER_PASSWORD')

    class Config:
        case_sensitive = True


settings = Settings()