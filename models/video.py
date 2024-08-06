
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
    Class:
        Video:
                Contains the Video model for teaching via video.
            It might contain elements like the amount of likes
            on a video or the amount of views or comments.

        :method __init__: Initializes the video class
    """
    __tablename__ = "videos"
    # Store a specific video data, likes, comments, views, e.t.c.
    # Also store the video resource (the VideoStatic) object which
    # contains metadata about the video to watch

    title = mapped_column(String(600), nullable=False)
    description = mapped_column(TEXT)

    video_id = mapped_column(ForeignKey("static_videos.id"))
    video = relationship("VideoStatic")

    bride_id = mapped_column(ForeignKey("bridges.id"))
    bridge = relationship("Bridge", back_populates="videos")

    thumbnail_id = mapped_column(ForeignKey("static_images.id"))
    thumbnail = relationship("ImageStatic")


    def __init__(self, **kwargs):
        required_keys = ["bridge_id", "video", "thumbnail", "title"]
        chk = self.check_required_keys(required_keys, **kwargs)
        if isinstance(chk, Error):
            "Required key(s) not present"
            return chk

        super().__init__()
        
        video = VideoStatic(video=kwargs["video"])
        thumbnail = ImageStatic(image=kwargs["thumbnail"])
        if isinstance(video, Error) or isinstance(thumbnail, Error):
            return Error(1001, "Video or Thumbnail named argument not found")
        
        video.save()
        thumbnail.save()
        video.refresh()
        thumbnail.refresh()

        kwargs["video_id"] = video.id
        kwargs["thumbnail_id"] = thumbnail.id
        del kwargs["video"]
        del kwargs["thumbnail"]
        [setattr(self, key, val) for key, val in kwargs.items()]
