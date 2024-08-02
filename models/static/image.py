
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import mapped_column

from models.basemodel import BaseModel
from models.base import Base

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
