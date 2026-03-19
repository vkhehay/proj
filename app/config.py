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

    # postgres_user: str
    # postgres_password: str
    # postgres_db: str

    # class Config:
    #     env_prefix = ""
    # import sys
    # import os
    #
    # sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    env_file: str = '.env'
    model_config = SettingsConfigDict(env_file=env_file)


settings = Settings()

#
# class Settings(BaseSettings):
#     db_port: int = Field(..., env="DB_PORT")
#     db_name: str = Field(..., env="DB_NAME")
#     db_password: str = Field(..., env="DB_PASSWORD")
#     db_username: str = Field(..., env="DB_USERNAME")
#     secret_key: str = Field(..., env="SECRET_KEY")
#     algorithm: str = Field(..., env="ALGORITHM")
#     access_token_exp_min: int = Field(..., env="ACCESS_TOKEN_EXP_MIN")
#     db_host: str = Field(..., env="DB_HOST")
#
#     # postgres_user: str = Field(..., env="POSTGRES_USER")
#     # postgres_password: str = Field(..., env="POSTGRES_PASSWORD")
#     # postgres_db: str = Field(..., env="POSTGRES_DB")
#
#     model_config = SettingsConfigDict(env_file=".env")
#
#     settings = Settings()
