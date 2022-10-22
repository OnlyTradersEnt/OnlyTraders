"""
    Create all your class based API here.This file can later be converted to a Python package if needed.

    NOTE: DO NOT IMPORT MAIN HERE TO AVOID CIRCULAR IMPORT ERROR
"""
from typing import List

from fastapi import Depends, UploadFile, File, Form
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from content.crud import UserCrud, PostCrud
from content.schemas.post import PostCreate, PostSearch, PostUpdate
from content.schemas.user import UserCreate, UserGet, UserUpdate, UserFilters
from content.service import MediaService, AuthenticationService
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
        self.media_service = MediaService(self.session)
        self.auth = AuthenticationService()

    @router.post("/create")
    def create_user(self, user: UserCreate):
        user.hashed_password = self.auth.get_password_hash(user.hashed_password)
        return self.crud.create_item(user)

    @router.get("/repository", response_model=List[UserGet])
    def read_users(self, limit: int = 100, filters: UserFilters = Depends()):
        users = self.crud.get_items(limit, **filters.dict(exclude_unset=True, exclude_none=True))
        return users

    @router.get("/{user_id}", response_model=UserGet)
    def read_user(self, user_id: int):
        db_user = self.crud.get_item(pk=user_id)
        return db_user

    @router.delete("/{user_id}")
    def delete_user(self, user_id: int):
        return self.crud.delete_item(user_id)

    @router.put("/{user_id}", response_model=UserGet)
    def update_user(self, user_id: int, params: UserUpdate):
        return self.crud.update_item(user_id, **params.dict(exclude_none=True, exclude_unset=True))

    @router.post("/{user_id}/add_dp", response_model=UserGet)
    def add_profile_pic(self, user_id: int, description: str = Form(''), file: UploadFile = File(...)):
        dp = self.media_service.upload_media(alt_text=description, file=file)
        user = self.crud.update_item(user_id, profile_pic_id=dp.get('id'))
        return user


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
        return post

    @router.delete("/{post_id}")
    def delete_post(self, post_id: int):
        return self.crud.delete_item(post_id)

    @router.put("/{post_id}")
    def update_post(self, post_id: int, params: PostUpdate):
        return self.crud.update_item(post_id, **params.dict(exclude_none=True, exclude_unset=True))


@cbv(router)
class MediaAPI:
    router.tags = ["media"]
    router.prefix = "/media"

    def __init__(self, session=Depends(get_db)):
        self.session = session
        self.media_service = MediaService(self.session)

    @router.post("/upload")
    def upload_file(self, description: str = Form(''), file: UploadFile = File(...)):
        return self.media_service.upload_media(description, file)

    @router.get('/{file_id}')
    def get_file(self, file_id: int):
        return self.media_service.get_media(file_id)
