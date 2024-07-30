
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.mysql import LONGTEXT

from ..basemodel import BaseModel, Base
from ..storage import Storage

class Blog(BaseModel, Base):
    __tablename__ = "blogs"
    __storage = Storage.storage


    author_id = mapped_column(ForeignKey("authors.user_id"), nullable=False)
    author = relationship("Author", back_populates="blogs")
    title = mapped_column(String(300), nullable=False)
    content = mapped_column(LONGTEXT, nullable=False)

    def __init__(self, **attrs: dict) -> None:
        [self.__setattr__(name, val) for name, val in attrs.items()]
        # Add object to the database session
        super().add()