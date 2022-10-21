from datetime import date
from typing import Optional, Union

from fastapi import Query, UploadFile, File
from pydantic import BaseModel, EmailStr


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


class UserGet(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    create_time: date
    profile_pic_id: int

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    """ Query params for update request """
    username: Optional[str]
    is_active: Optional[bool]