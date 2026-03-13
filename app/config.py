# import os
# from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


# BASE_DIR = Path(__file__).resolve().parent.parent  # корень проекта
# ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    db_url: str
    db_port: int
    db_name: str
    db_password: str
    db_username: str
    secret_key: str
    algorithm: str
    access_token_exp_min: int

    model_config = SettingsConfigDict(env_file=".env")
    # model_config = SettingsConfigDict(env_file=str(ENV_PATH))


settings = Settings()

