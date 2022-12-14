""" Create all models here """
from datetime import date

from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey, LargeBinary
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

    profile_pic_id = Column(Integer, ForeignKey('media.id', ondelete='SET NULL'), nullable=True)
    profile_pic = relationship("Media")

    posts = relationship('Post', back_populates='creator')
    comments = relationship('Comment', back_populates='creator')


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    creator = relationship('User', back_populates='posts')

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    comments = relationship('Comment', back_populates='post')


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)

    creator_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    creator = relationship('User', back_populates='comments')

    post_id = Column(Integer, ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    post = relationship('Post', back_populates='comments')