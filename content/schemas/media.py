from pydantic import BaseModel


class MediaCreate(BaseModel):
    """ Query params for create request """
    filename: str
    blob: bytes
    alt_text: str
    content_type: str