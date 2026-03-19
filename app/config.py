import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


# class Settings(BaseSettings):
#     db_port: int
#     db_name: str
#     db_password: str
#     db_username: str
#     secret_key: str
#     algorithm: str
#     access_token_exp_min: int
#     db_host: str  # = "db"
#
#     env_file: str = '.env'
#     model_config = SettingsConfigDict(env_file=env_file)

class Settings(BaseSettings):
    db_port: int = Field(..., alias="DB_PORT")
    db_name: str = Field(..., alias="DB_NAME")
    db_password: str = Field(..., alias="DB_PASSWORD")
    db_username: str = Field(..., alias="DB_USERNAME")
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_exp_min: int = Field(..., alias="ACCESS_TOKEN_EXP_MIN")
    db_host: str = Field(..., alias="DB_HOST")

    model_config = SettingsConfigDict(env_file=".env", populate_by_name=True)


settings = Settings()

