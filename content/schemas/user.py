from datetime import date
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, EmailStr


# properties required during user creation
class UserCreate(BaseModel):
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
