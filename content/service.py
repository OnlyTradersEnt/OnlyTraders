import os

from fastapi import UploadFile
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from content.crud import MediaCrud
from content.schemas.media import MediaCreate
from io import BytesIO


class MediaService:

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
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)
