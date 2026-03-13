from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg2
from .config import settings

Base = declarative_base()

DATABASE_URL = f'postgresql://{settings.db_username}:{settings.db_password}@{settings.db_url}:{settings.db_port}/{settings.db_name}'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, bind=engine)


def get_db():
    with SessionLocal() as db:
        yield db


check = settings.db_url

if __name__ == '__main__':
    print(check)