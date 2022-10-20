""" Create all models here """
from datetime import date

from sqlalchemy import Boolean, Column, Integer, String, Date, BLOB, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship

from db import Base


# IMP: EVERY MODEL MUST HAVE 'id' ATTRIBUTE

class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    blob = Column(LargeBinary, nullable=False)
    alt_text = Column(String, nullable=True)
    content_type = Column(String, nullable=False)

    def to_dict(self):
        return {
                'id': self.id,
                'filename': self.filename,
                'description': self.alt_text,
                'content_type': self.content_type,
        }


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    create_time = Column(Date, nullable=False, default=date.today())


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
