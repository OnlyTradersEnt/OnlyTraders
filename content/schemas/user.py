from datetime import date
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """ properties required during user creation """
    username: str
    email: EmailStr
    hashed_password: str
    create_time: date


class UserGet(BaseModel):
    """ Query params for GET request """
    id: Optional[int] = Query(alias='pk')
    username: Optional[str] = Query(alias="name")
    is_active: Optional[bool] = Query()
    create_time: Optional[date] = Query()


class UserUpdate(BaseModel):
    """ Query params for update request """
    username: Optional[str]
    is_active: Optional[bool]