from typing import Optional

from fastapi import Query
from pydantic import BaseModel


class PostBase(BaseModel):
    """ properties required during post creation """
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None


class PostCreate(PostBase):
    title: str
    description: str


class PostSearch(BaseModel):
    """ Query params for get request"""
    id: Optional[int] = Query(alias='pk')
    title: Optional[str] = Query(alias="subject")


class PostUpdate(BaseModel):
    """ Query params for update request"""
    title: Optional[str]
    description: Optional[str]
