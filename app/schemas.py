from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # Use default value for optional parameter
    # rating: Optional[int] = None  # USe Optional import from typing


class PostCreate(PostBase):
    pass


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: str
    dir: conint(le=1)
