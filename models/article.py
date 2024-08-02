
from sqlalchemy import String, ForeignKey, Integer, Table, Column
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.mysql import TEXT

from models.basemodel import BaseModel
from models.base import Base


article_images = Table(
    "article_images",
    Base.metadata,
    Column("article_id", ForeignKey("articles.id"), primary_key=True),
    Column("image_id", ForeignKey("static_images.id"), primary_key=True)
)

article_videos = Table(
    "article_videos",
    Base.metadata,
    Column("article_id", ForeignKey("articles.id"), primary_key=True),
    Column("video_id", ForeignKey("static_videos.id"), primary_key=True)
)

class Article(BaseModel, Base):
    __tablename__ = "articles"

    title = mapped_column(String(300), nullable=False)
    content = mapped_column(TEXT, nullable=False)
    views = mapped_column(Integer, default=0, nullable=False)
    bridge_id = mapped_column(ForeignKey("bridges.id"))
    bridge = relationship("Bridge", back_populates="articles")

    images = relationship("ImageStatic", secondary=article_images)
    videos = relationship("VideoStatic", secondary=article_videos)