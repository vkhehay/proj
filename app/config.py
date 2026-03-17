import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_port: int
    db_name: str
    db_password: str
    db_username: str
    secret_key: str
    algorithm: str
    access_token_exp_min: int
    db_host: str  # = "db"

    postgres_user: str
    postgres_password: str
    postgres_db: str

    # env_file: str = ".env" if os.getenv("ENV") != "test" else ".env.test"
    env_file: str = '.env'

    model_config = SettingsConfigDict(env_file=env_file)


settings = Settings()
