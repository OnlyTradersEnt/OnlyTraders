from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class PostCreate(PostBase):
    title: str
    description: str


# this will be used to format the response to not to have id,owner_id etc
class ShowPost(PostBase):
    title: str
    description: Optional[str]

    class Config():  # to convert non dict obj to json
        orm_mode = True
