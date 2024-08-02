
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.mysql import TINYTEXT

from models.basemodel import BaseModel
from models.base import Base

class Bridge(BaseModel, Base):
    __tablename__ = "bridges"
    name = mapped_column(String(300), nullable=False)
    description = mapped_column(TINYTEXT)
    image_id = mapped_column(ForeignKey("static_images.id"))
    image = relationship("ImageStatic")

    articles = relationship("Article", back_populates="bridge")
    videos = relationship("Video", back_populates="bridge")
    user = relationship("User", back_populates="bridge")

    def __init__(self, **attrs: dict) -> None:
        super().__init__()
        [setattr(self, key, value) for key, value in attrs.items()]
