
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import mapped_column, relationship

from models.basemodel import BaseModel
from models.base import Base

class Video(BaseModel, Base):
    """Contains the Video model for teaching via video.
        It might contain elements like the amount of
        likes on a video or the amount of views or comments.
    """
    __tablename__ = "videos"
    # Store video metadata. Whatever is needed to
    # access the video from youtube

    # metadata to access video from youtube
    bride_id = mapped_column(ForeignKey("bridges.id"))
    bridge = relationship("Bridge", back_populates="videos")

