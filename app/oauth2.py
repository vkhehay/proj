import jwt
# from jwt.exceptions import InvalidTokenError
from jwt import PyJWTError
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from .schema import TokenData
from .database import get_db, SessionLocal
from .models import User

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXP_TIME = settings.access_token_exp_min

oath2_schema = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict, ):
    to_encode = data.copy()

    expired_time = datetime.now(timezone.utc) + timedelta(minutes=EXP_TIME)
    to_encode.update({"exp": expired_time})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)
    except PyJWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oath2_schema), db: SessionLocal = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})

    # return verify_access_token(token, credentials_exception) Возвращает "id="id

    token = verify_access_token(token, credentials_exception)
    user_id = (db.query(User)
               .filter(User.id == token.id)
               .first())  # Дополнительная проверка на наличие юзера  в базе

    return user_id.id  # Возвращаем id по атрибуту из ORM int(id)
