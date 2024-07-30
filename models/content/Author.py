from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, relationship

from ..basemodel import BaseModel, Base
from ..storage import Storage

class Author(BaseModel, Base):
    __tablename__ = "authors"
    __storage = Storage.storage

    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    user = relationship("User")
    # blogs
    blogs = relationship("Blog", back_populates="author")
    # videos
    videos = relationship("Video", back_populates="author")

    def __init__(self, **attrs: dict) -> None:
        [self.__setattr__(name, val) for name, val in attrs.items()]
        # Add object to the database session
        super().add()
