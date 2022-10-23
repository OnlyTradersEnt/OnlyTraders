from datetime import date
from typing import Optional, Union

from fastapi import Query
from pydantic import BaseModel, EmailStr
from content.schemas.media import ShowMedia


class UserCreate(BaseModel):
    """ properties required during user creation """
    username: str
    email: EmailStr
    hashed_password: str
    create_time: date


class UserFilters(BaseModel):
    """ Query params for GET request """
    id: Optional[int] = Query(alias='pk')
    username: Optional[str] = Query(alias="name")
    is_active: Optional[bool] = Query()
    create_time: Optional[date] = Query()


class ShowUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    create_time: date
    profile_pic: Optional[ShowMedia] = None

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    """ Query params for update request """
    username: Optional[str]
    is_active: Optional[bool]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
