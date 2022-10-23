from typing import Optional

from pydantic.main import BaseModel


class CommentCreate(BaseModel):
    text: str
    post_id: int
    creator_id: int


class ShowComment(BaseModel):
    id: int
    text: str
    creator_id: int
    post_id: int

    class Config:
        orm_mode = True


class CommentSearch(BaseModel):
    id: Optional[int]
    post_id: Optional[int]
    creator_id: Optional[int]


class CommentUpdate(BaseModel):
    text: str
