"""
    Create all operations required for APIs here.

    todo : why does CRUD operations need to be specific? can't we create generic CRUD operations?

    Basic Interface for CRUD  -> Generic CRUD operations class
                                        |-inherit
    Specific model operations -> class that extends the CRUD operations
"""

from pydantic.main import BaseModel
from sqlalchemy.orm import Session

from db import Base
from .models import User, Post


class AbstractCrud:
    model: Base = NotImplemented
    session: Session = NotImplemented

    def get_items(self, limit,  **filters):
        """ Read operation """
        if not filters:
            return []
        return self.session.query(self.model).filter_by(**filters).limit(limit).all()

    def get_item(self, pk: int):
        return self.session.query(self.model).get(pk)

    def create_item(self, obj: BaseModel):
        """ Create operation """
        db_item = self.model(**obj.dict())
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return db_item

    def update_item(self, *args, **kwargs):
        """ Update operation"""
        # todo
        NotImplemented

    def delete_item(self, pk: int):
        """ Delete operation """
        q = self.session.query(self.model).filter(self.model.id == pk).delete()
        self.session.commit()
        return q


class UserCrud(AbstractCrud):

    def __init__(self, session: Session):
        self.session = session
        self.model = User


class PostCrud(AbstractCrud):

    def __init__(self, session: Session):
        self.session = session
        self.model = Post
