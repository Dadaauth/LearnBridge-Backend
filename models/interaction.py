
from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import mapped_column

from models.basemodel import BaseModel
from models.base import Base


class ArticleInteraction(BaseModel, Base):
    """ """
    __tablename__ = "article_interactions"

    like = mapped_column(Boolean, nullable=True)
    dislike = mapped_column(Boolean, nullable=True)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    article_id = mapped_column(ForeignKey("articles.id"), nullable=False)


class VideoInteraction(BaseModel, Base):
    """ """
    __tablename__ = "video_interactions"

    like = mapped_column(Boolean, nullable=True)
    dislike = mapped_column(Boolean, nullable=True)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    video_id = mapped_column(ForeignKey("videos.id"), nullable=False)

