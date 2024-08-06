
from models.basemodel import BaseModel
from models.base import Base

from lib.error import Error

class VideoStatic(BaseModel, Base):
    """Contains the metadata for videos on the website
    This video table only holds static videos uploaded
    to the website. It does not hold videos from youtube
    """
    __tablename__ = "static_videos"
    # Store video metadata. Whatever is needed to
    # access the video from the cloud storage
    
    # Many-To-Many relationship. Other Objects should
    # be able to hold several videos. And The videos
    # can belong to several objects

    def __init__(self, **kwargs):
        """
            :params video: a python file object representing the video to store.
            :param 
        """
        required_keys = ["video"]
        chk = self.check_required_keys(required_keys, **kwargs)
        if isinstance(chk, Error):
            "Required key(s) not present"
            return chk

        super().__init__()