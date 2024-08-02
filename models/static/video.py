
from models.basemodel import BaseModel
from models.base import Base

class VideoStatic(BaseModel, Base):
    """Contains the metadata for videos on the website
    This video table only holds static videos uploaded
    to the website. It does not hold videos from youtube
    """
    __tablename__ = "static_videos"
    # Store video metadata. Whatever is needed to
    # access the video from the storage engine
    
    # Many-To-Many relationship. Other Objects should
    # be able to hold several videos. And The videos
    # can belong to several objects