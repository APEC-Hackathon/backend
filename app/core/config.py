import secrets

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    PROJECT_NAME: str = 'Kebab API'

    class Config:
        case_sensitive = True


settings = Settings()
