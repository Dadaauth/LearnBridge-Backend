
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.mysql import TEXT

from models.basemodel import BaseModel
from models.base import Base


class Video(BaseModel, Base):
    """
    """
    __tablename__ = "videos"
    
    title = mapped_column(String(300), nullable=False)
    description = mapped_column(TEXT, nullable=False)
    thumbnail = mapped_column(String(300), nullable=False)
    source_id = mapped_column(ForeignKey("users.id"), nullable=False)
    course_id = mapped_column(ForeignKey("courses.id"), nullable=False)
    object_name = mapped_column(String(60), nullable=False)


    def __init__(self, *args, **kwargs) -> None:
        """
        """
        super().__init__()
        [setattr(self, key, value) for key, value in kwargs.items()]
        self.source_id = self.user_id

