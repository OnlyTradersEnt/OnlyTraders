import os
from datetime import timedelta, datetime
from io import BytesIO
from typing import Union

from fastapi import UploadFile, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import settings
from content.crud import MediaCrud, UserCrud
from content.exceptions import CredentialsException
from content.models import User
from content.schemas.media import MediaCreate
from content.schemas.user import TokenData
from db import get_db


class MediaService:
    """ Service to handle all types of Media """

    def __init__(self, session: Session, *args, **kwargs):
        self.crud = MediaCrud(session)

    def upload_media(self, alt_text: str, file: UploadFile, *args, **kwargs):
        data = file.file.read()
        item = MediaCreate(filename=file.filename, content_type=file.content_type, blob=data, alt_text=alt_text)
        obj = self.crud.create_item(item)
        return obj.to_dict()

    def get_media(self, pk: int, *args, **kwargs):
        obj = self.crud.get_item(pk)
        path = f'media/{obj.filename}'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(BytesIO(obj.blob).getbuffer())  # noqa
        return {**obj.to_dict(), 'filepath': os.path.abspath(path)}


class AuthenticationService:
    """ Authentication and Authorization Service. """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.LOGIN_URL)

    @classmethod
    def get_password_hash(cls, password: str):
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain: str, hashed: str):
        return cls.pwd_context.verify(plain, hashed)

    @classmethod
    def authenticate_user(cls, request: OAuth2PasswordRequestForm, user: User):
        if not user:
            raise CredentialsException
        if not AuthenticationService.verify_password(request.password, user.hashed_password):
            raise CredentialsException
        return True

    @classmethod
    def create_access_token(
            cls, data: dict,
            expires_delta: Union[timedelta, None] = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    ):
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @classmethod
    async def get_current_user(cls, session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise CredentialsException
            token_data = TokenData(username=username)
        except JWTError:
            raise CredentialsException
        user = UserCrud(session).get_user(username=token_data.username)
        if user is None:
            raise CredentialsException
        return user
