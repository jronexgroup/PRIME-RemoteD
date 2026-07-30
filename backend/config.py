import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = ""
    ALLOWED_TELEGRAM_USER_IDS: list[int] = []
    API_KEY: str = ""
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    POLL_TIMEOUT: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @classmethod
    def parse_user_ids(cls, v: str | list) -> list[int]:
        if isinstance(v, str):
            return [int(uid.strip()) for uid in v.split(",") if uid.strip()]
        return v


settings = Settings()

if settings.ALLOWED_TELEGRAM_USER_IDS and isinstance(settings.ALLOWED_TELEGRAM_USER_IDS, str):
    settings.ALLOWED_TELEGRAM_USER_IDS = Settings.parse_user_ids(settings.ALLOWED_TELEGRAM_USER_IDS)
