import secrets

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    
    PROJECT_NAME: str = 'Kebab API'

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days

    SQLALCHEMY_DATABASE_URI: str = "postgresql://postgres:password@db:5432/app"
    # SQLALCHEMY_DATABASE_URI: str = "sqlite:///./app.db"e

    FIRST_SUPERUSER: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "password"

    class Config:
        case_sensitive = True


settings = Settings()