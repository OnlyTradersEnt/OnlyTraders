from pydantic import BaseModel


class MediaCreate(BaseModel):
    """ Query params for update request """
    filename: str
    blob: bytes
    alt_text: str
    content_type: str


class MediaGet(BaseModel):
    """ Query params for update request """
    id: int
    filename: str
    alt_text: str
    content_type: str