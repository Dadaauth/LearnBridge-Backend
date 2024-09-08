
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.mysql import TEXT

from models.basemodel import BaseModel
from models.base import Base
from models.static.video import VideoStatic
from models.static.image import ImageStatic

from lib.error import Error

class Video(BaseModel, Base):
    """
    """
    __tablename__ = "videos"
    
    title = mapped_column(String(300), nullable=False)
    description = mapped_column(TEXT, nullable=False)
    thumbnail = mapped_column(String(300), nullable=False)
    source_id = mapped_column(ForeignKey("users.id"), nullable=False)
    course_id = mapped_column(ForeignKey("courses.id"), nullable=False)