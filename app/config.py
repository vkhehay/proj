import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    db_port: int
    db_name: str
    db_password: str
    db_username: str
    secret_key: str
    algorithm: str
    access_token_exp_min: int
    db_host: str  # = "db"

    env_file: str = '.env'
    model_config = SettingsConfigDict(env_file=env_file)


settings = Settings()

