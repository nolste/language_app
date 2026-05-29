from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    database_url: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        extra="ignore"
    )


@lru_cache
def get_settings():
    print(f"Looking for env file at: {ENV_FILE}")
    print(f"Exists: {ENV_FILE.exists()}")

    return Settings()


settings = get_settings()
