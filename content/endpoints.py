"""
    Create all your class based API here.This file can later be converted to a Python package if needed.

    NOTE: DO NOT IMPORT MAIN HERE TO AVOID CIRCULAR IMPORT ERROR
"""

from fastapi import Depends, HTTPException
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from content.crud import UserCrud, PostCrud
from content.schemas.post import PostCreate, PostSearch
from content.schemas.user import UserCreate, UserGet
from db import get_db

router = InferringRouter()  # import this router in main and include it in app


# todo create generic crud apis?
# todo add documentation

@cbv(router)
class UserAPI:
    router.tags = ["User"]
    router.prefix = "/users"

    def __init__(self, session=Depends(get_db)):
        self.session = session
        self.crud = UserCrud(self.session)

    @router.post("/create")
    def create_user(self, user: UserCreate):
        return self.crud.create_item(user)

    @router.get("/repository")
    def read_users(self, limit: int = 100,  filters: UserGet = Depends()):
        users = self.crud.get_items(limit, **filters.dict(exclude_unset=True, exclude_none=True))
        return users

    @router.get("/{user_id}")
    def read_user(self, user_id: int):
        db_user = self.crud.get_item(pk=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user

    @router.delete("/{user_id}")
    def delete_user(self, user_id: int):
        self.crud.delete_item(user_id)


@cbv(router)
class PostAPI:
    router.tags = ["Post"]
    router.prefix = "/posts"

    def __init__(self, session=Depends(get_db)):
        self.session = session
        self.crud = PostCrud(self.session)

    @router.post("/create")
    def create_post(self, post: PostCreate):
        return self.crud.create_item(post)

    @router.get("/repository")
    def read_posts(self, limit: int = 100, filters: PostSearch = Depends()):
        posts = self.crud.get_items(limit, **filters.dict(exclude_none=True, exclude_unset=True))
        return posts

    @router.get("/{post_id}")
    def read_post(self, post_id: int):
        post = self.crud.get_item(pk=post_id)
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

    @router.delete("/{post_id}")
    def delete_post(self, post_id: int):
        self.crud.delete_item(post_id)
