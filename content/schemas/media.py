from pydantic import BaseModel


class MediaCreate(BaseModel):
    """ Query params for create request """
    filename: str
    blob: bytes
    alt_text: str
    content_type: str


class ShowMedia(BaseModel):
    id: int
    filename: str
    alt_text: str
    content_type: str

    class Config:
        orm_mode = True
