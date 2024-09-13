
from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from models.basemodel import BaseModel
from models.base import Base


class Course(BaseModel, Base):
    """ """
    __tablename__ = "courses"

    title = mapped_column(String(300), nullable=False)
    code = mapped_column(String(45), nullable=False)
    thumbnail = mapped_column(String(300), nullable=True)
    instructor = mapped_column(String(300), nullable=False)

    def __init__(self,*args, **kwargs) -> None:
        """
        """
        super().__init__()
        [setattr(self, key, value) for key, value in kwargs.items()]
