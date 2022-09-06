from datetime import date

from pydantic import BaseModel, EmailStr


# properties required during user creation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    create_time: date


class ShowUser(BaseModel):
    username: str
    email: EmailStr
    is_active: bool
    create_time: date

    class Config:  # tells pydantic to convert even non dict obj to json
        orm_mode = True
