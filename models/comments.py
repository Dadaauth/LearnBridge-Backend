
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.mysql import TINYTEXT

from models.basemodel import BaseModel
from models.base import Base


class ArticleComments(BaseModel, Base):
    """ """
    __tablename__ = "article_comments"

    content = mapped_column(TINYTEXT, nullable=False)
    interaction_id = mapped_column(ForeignKey("article_interactions.id"), nullable=False)



class VideoComments(BaseModel, Base):
    """ """
    __tablename__ = "video_comments"

    content = mapped_column(TINYTEXT, nullable=False)
    interaction_id = mapped_column(ForeignKey("video_interactions.id"), nullable=False)