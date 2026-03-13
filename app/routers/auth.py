from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schema, models, hashing, oauth2
# from database import get_db
# from schema import Token
# from models import User
# from hashing import verify_password
# from oauth2 import create_access_token

get_db = database.get_db
User = models.User
Token = schema.Token
verify_password = hashing.verify_password
create_access_token = oauth2.create_access_token

router = APIRouter(
    tags=["Authentification"]
)

@router.post('/login', response_model=Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):

    login = db.query(User).filter(User.email==user.username).first()

    if not login:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Wrong email or password')

    if not verify_password(user.password, login.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Wrong password')

    access_token = create_access_token(data = {"user_id":login.id})

    return {"access_token": access_token, "token_type": "bearer"}
