from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

# 1. Define your settings schema
class Settings(BaseSettings):
    database_url: str

    # Tell Pydantic to read from a .env file
    model_config = SettingsConfigDict(env_file=".env")

# 2. Use lru_cache so the .env file is only read once from the disk
@lru_cache
def get_settings():
    return Settings()


