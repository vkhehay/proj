from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic import conint
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(UserCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserOut(BaseModel):
    name: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = False


class PostResponse(PostCreate):
    id: int
    created_at: datetime
    owner: UserOut
    model_config = ConfigDict(from_attributes=True)


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published: bool = False
    created_at: datetime
    owner: UserOut
    model_config = ConfigDict(from_attributes=True)


class PostVote(BaseModel):
    post: PostOut
    votes: int
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class VoteResponse(BaseModel):
    post_id: int
    dir: conint(le=1)

    # model_config = ConfigDict(from_attributes=True)


class VoteMessage(BaseModel):
    message: str
