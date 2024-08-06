
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import mapped_column

from models.basemodel import BaseModel
from models.base import Base

from lib.error import Error

class ImageStatic(BaseModel, Base):
    """
        It should contain images metadata,
        Other tables or elements can link
        to it to access their image metadata
    """
    __tablename__ = "static_images"

    # Store image metadata. Whatever is needed to
    # access the image from the storage engine

    # Many-To-Many relationship. Other Objects should
    # be able to hold several images. And The images
    # can belong to several objects


    def __init__(self, **kwargs):
        required_keys = ["image"]
        chk = self.check_required_keys(required_keys, **kwargs)
        if isinstance(chk, Error):
            return chk
        
        super().__init__()

        # 
