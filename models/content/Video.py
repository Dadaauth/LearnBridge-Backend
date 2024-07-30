
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship

from ..basemodel import Base, BaseModel

class Video(BaseModel, Base):
    __tablename__ = "videos"

    author_id = mapped_column(ForeignKey("authors.user_id"), nullable=False)
    author = relationship("Author", back_populates="videos")
    title = mapped_column(String(300), nullable=False)

    def __init__(self, **attrs: dict) -> None:
        [self.__setattr__(name, val) for name, val in attrs.items()]
        # Add object to the database session
        super().add()