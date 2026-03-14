from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, database, schema, hashing

User = models.User
get_db = database.get_db
UserCreate = schema.UserCreate
UserResponse = schema.UserResponse
UserUpdate = schema.UserUpdate
UserOut = schema.UserOut
hash_password = hashing.hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_data = user.dict()
    user_data["password"] = hash_password(user.password)

    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=UserOut)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    query = (db.query(User).filter(User.id == user_id))
    user_new = user.dict()
    user_new["password"] = hash_password(user.password)
    query.update(user_new, synchronize_session=False)
    db.commit()
    updated_user = query.first()
    return updated_user


@router.get('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=UserOut)
def get_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such user')
    return user
