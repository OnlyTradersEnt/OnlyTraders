"""
    Create all your class based API here.This file can later be converted to a Python package if needed.

    NOTE: DO NOT IMPORT MAIN HERE TO AVOID CIRCULAR IMPORT ERROR
"""

from fastapi import Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from content.crud import UserCrud, PostCrud
from content.schemas.post import PostCreate
from content.schemas.user import UserCreate
from db import get_db

router = InferringRouter()  # import this router in main and include it in app

# todo remove repetitive tag assignments
# todo create generic crud apis?
# todo add documentation


@cbv(router)
class UserAPI:

    def __init__(self, session=Depends(get_db)):
        self.session = session
        self.crud = UserCrud(self.session)

    @router.post("/user", tags=['User'])
    def create_user(self, user: UserCreate):
        return self.crud.create_item(user)

    @router.get("/users/", tags=['User'])
    def read_users(self, skip: int = 0, limit: int = 100):
        users = self.crud.get_items(skip, limit)
        return users

    @router.get("/users/{user_id}", tags=['User'])
    def read_user(self, user_id: int):
        db_user = self.crud.get_item(pk=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user

    @router.delete("/users/{user_id}", tags=['User'])
    def delete_user(self, user_id: int):
        self.crud.delete_item(user_id)


@cbv(router)
class PostAPI:
    def __init__(self, session=Depends(get_db)):
        self.session = session
        self.crud = PostCrud(self.session)

    @router.post("/post", tags=['Posts'])
    def create_post(self, post: PostCreate):
        return self.crud.create_item(post)

    @router.get("/posts/", tags=['Posts'])
    def read_users(self, skip: int = 0, limit: int = 100):
        posts = self.crud.get_items(skip, limit)
        return posts

    @router.get("/posts/{post_id}", tags=['Posts'])
    def read_user(self, post_id: int):
        post = self.crud.get_item(pk=post_id)
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

    @router.delete("/posts/{post_id}", tags=['Posts'])
    def delete_user(self, post_id: int):
        self.crud.delete_item(post_id)
