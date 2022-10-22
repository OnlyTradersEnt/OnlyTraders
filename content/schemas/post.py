from typing import Optional

from fastapi import Query
from pydantic import BaseModel


class PostBase(BaseModel):
    """ properties required during post creation """
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    creator_id: int


class PostCreate(BaseModel):
    title: str
    description: str
    creator_id: int


class PostSearch(BaseModel):
    """ Query params for get request"""
    id: Optional[int] = Query(alias='pk')
    title: Optional[str] = Query(alias="subject")
    creator_id: Optional[int] = Query(alias='user')


class PostUpdate(BaseModel):
    """ Query params for update request"""
    title: Optional[str]
    description: Optional[str]


class ShowPost(PostBase):

    class Config:
        orm_mode = True
