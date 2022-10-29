"""
    Create all your class based API here.This file can later be converted to a Python package if needed.

    NOTE: DO NOT IMPORT MAIN HERE TO AVOID CIRCULAR IMPORT ERROR
"""
from typing import List

from fastapi import Depends, UploadFile, File, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from content.crud import UserCrud, PostCrud, CommentCrud
from content.models import User
from content.schemas.comment import ShowComment, CommentSearch, CommentUpdate, CommentCreate
from content.schemas.post import PostCreate, PostSearch, PostUpdate, ShowPost
from content.schemas.user import UserCreate, UserUpdate, UserFilters, ShowUser, Token
from content.service import MediaService, AuthenticationService
from db import get_db

router = InferringRouter()  # import this router in main and include it in app


# todo create generic crud apis?
# todo add documentation
# todo use different router for each API class?

@cbv(router)
class AuthAPI:
    router.tags = ['Authentication']
    router.prefix = '/auth'

    def __init__(self, session=Depends(get_db)):
        self.session = session
        self.crud = UserCrud(self.session)

    @router.post('/login', response_model=Token)
    async def login(self, request: OAuth2PasswordRequestForm = Depends()):
        user = self.crud.get_user(username=request.username)
        AuthenticationService.authenticate_user(request, user)
        access_token = AuthenticationService.create_access_token(data={"sub": user.username})
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    @router.post('/signup', response_model=Token)
    async def signup(self, user: UserCreate):
        user.hashed_password = AuthenticationService.get_password_hash(user.hashed_password)
        user = self.crud.create_item(user)
        access_token = AuthenticationService.create_access_token(data={"sub": user.username})
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    # todo add logout endpoint to invalidate token?


@cbv(router)
class UserAPI:
    router.tags = ["User"]
    router.prefix = "/users"

    def __init__(self, session=Depends(get_db), user: User = Depends(AuthenticationService.get_current_user)):
        self.session = session
        self.crud = UserCrud(self.session)
        self.media_service = MediaService(self.session)

    @router.post("/create")
    async def create_user(self, user: UserCreate):
        user.hashed_password = AuthenticationService.get_password_hash(user.hashed_password)
        return self.crud.create_item(user)

    @router.get("/repository", response_model=List[ShowUser])
    async def read_users(self, limit: int = 100, filters: UserFilters = Depends()):
        users = self.crud.get_items(limit, **filters.dict(exclude_unset=True, exclude_none=True))
        return users

    @router.get("/{user_id}", response_model=ShowUser)
    async def read_user(self, user_id: int):
        db_user = self.crud.get_item(pk=user_id)
        return db_user

    @router.delete("/{user_id}")
    async def delete_user(self, user_id: int):
        return self.crud.delete_item(user_id)

    @router.put("/{user_id}", response_model=ShowUser)
    async def update_user(self, user_id: int, params: UserUpdate):
        return self.crud.update_item(user_id, **params.dict(exclude_none=True, exclude_unset=True))

    @router.post("/{user_id}/add_dp", response_model=ShowUser)
    async def add_profile_pic(self, user_id: int, description: str = Form(''), file: UploadFile = File(...)):
        dp = self.media_service.upload_media(alt_text=description, file=file)
        user = self.crud.update_item(user_id, profile_pic_id=dp.get('id'))
        return user

    @router.get('/{user_id}/all_posts', response_model=List[ShowPost])
    async def get_user_posts(self, user_id: int, limit: int = 100):
        user = self.crud.get_item(user_id)
        return user.posts  # todo need to use limit here

    @router.get('/{user_id}/all_comments', response_model=List[ShowComment])
    async def get_user_comments(self, user_id: int, limit: int = 100):
        user = self.crud.get_item(user_id)
        return user.comments  # todo need to use limit here

    @router.get("/users/me/", response_model=ShowUser)
    async def get_current_user(self, current_user: User = Depends(AuthenticationService.get_current_user)):
        return current_user


@cbv(router)
class PostAPI:
    router.tags = ["Post"]
    router.prefix = "/posts"

    def __init__(self, session=Depends(get_db), user: User = Depends(AuthenticationService.get_current_user)):
        self.session = session
        self.crud = PostCrud(self.session)

    @router.post("/create")
    async def create_post(self, post: PostCreate):
        return self.crud.create_item(post)

    @router.get("/repository", response_model=List[ShowPost])
    async def read_posts(self, limit: int = 100, filters: PostSearch = Depends()):
        posts = self.crud.get_items(limit, **filters.dict(exclude_none=True, exclude_unset=True))
        return posts

    @router.get("/{post_id}", response_model=ShowPost)
    async def read_post(self, post_id: int):
        post = self.crud.get_item(pk=post_id)
        return post

    @router.delete("/{post_id}")
    async def delete_post(self, post_id: int):
        return self.crud.delete_item(post_id)

    @router.put("/{post_id}")
    async def update_post(self, post_id: int, params: PostUpdate):
        return self.crud.update_item(post_id, **params.dict(exclude_none=True, exclude_unset=True))

    @router.get("/{post_id}/comments", response_model=List[ShowComment])
    async def get_comments(self, post_id: int, limit: int = 100):
        post = self.crud.get_item(post_id)
        return post.comments


@cbv(router)
class CommentAPI:
    router.tags = ["Comment"]
    router.prefix = "/comments"

    def __init__(self, session=Depends(get_db), user: User = Depends(AuthenticationService.get_current_user)):
        self.session = session
        self.crud = CommentCrud(self.session)

    @router.post("/create")
    async def create_comment(self, comment: CommentCreate):
        return self.crud.create_item(comment)

    @router.get("/repository", response_model=List[ShowComment])
    async def read_comments(self, limit: int = 100, filters: CommentSearch = Depends()):
        comments = self.crud.get_items(limit, **filters.dict(exclude_none=True, exclude_unset=True))
        return comments

    @router.get("/{comment_id}", response_model=ShowComment)
    async def read_comment(self, post_id: int):
        comment = self.crud.get_item(pk=post_id)
        return comment

    @router.delete("/{comment_id}")
    async def delete_comment(self, comment_id: int):
        return self.crud.delete_item(comment_id)

    @router.put("/{comment_id}")
    async def update_comment(self, comment_id: int, params: CommentUpdate):
        return self.crud.update_item(comment_id, **params.dict(exclude_none=True, exclude_unset=True))


@cbv(router)
class MediaAPI:
    router.tags = ["media"]
    router.prefix = "/media"

    def __init__(self, session=Depends(get_db), user: User = Depends(AuthenticationService.get_current_user)):
        self.session = session
        self.media_service = MediaService(self.session)

    @router.post("/upload")
    async def upload_file(self, description: str = Form(''), file: UploadFile = File(...)):
        return self.media_service.upload_media(description, file)

    @router.get('/{file_id}')
    async def get_file(self, file_id: int):
        return self.media_service.get_media(file_id)
