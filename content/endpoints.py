"""
    Create all your class based API here.This file can later be converted to a Python package if needed.

    NOTE: DO NOT IMPORT MAIN HERE TO AVOID CIRCULAR IMPORT ERROR
"""
import os
from io import BytesIO

from fastapi import Depends, UploadFile, File, Form, HTTPException
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from content.crud import UserCrud, PostCrud, MediaCrud
from content.schemas.media import MediaCreate
from content.schemas.post import PostCreate, PostSearch, PostUpdate
from content.schemas.user import UserCreate, UserGet, UserUpdate
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
    def read_users(self, limit: int = 100, filters: UserGet = Depends()):
        users = self.crud.get_items(limit, **filters.dict(exclude_unset=True, exclude_none=True))
        return users

    @router.get("/{user_id}")
    def read_user(self, user_id: int):
        db_user = self.crud.get_item(pk=user_id)
        return db_user

    @router.delete("/{user_id}")
    def delete_user(self, user_id: int):
        return self.crud.delete_item(user_id)

    @router.put("/{user_id}")
    def update_user(self, user_id: int, params: UserUpdate):
        return self.crud.update_item(user_id, **params.dict(exclude_none=True, exclude_unset=True))


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
        self.crud = MediaCrud(self.session)

    @router.post("/upload")
    def upload_file(self, description: str = Form(''), file: UploadFile = File(...)):
        try:
            data = file.file.read()
            name = file.filename
            content_type = file.content_type
            item = MediaCreate(filename=name, content_type=content_type, blob=data, alt_text=description)
            obj = self.crud.create_item(item)
        except Exception as e:
            return HTTPException(500, "Could not upload media")

        return obj.to_dict()

    @router.get('/{file_id}')
    def get_file(self, file_id: int):
        obj = self.crud.get_item(file_id)
        path = f'media/{obj.filename}'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(BytesIO(obj.blob).getbuffer())  # noqa
        return {**obj.to_dict(), 'filepath': os.path.abspath(path)}
