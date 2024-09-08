
from sqlalchemy import String, ForeignKey, Integer, Table, Column
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.mysql import TEXT

from models.basemodel import BaseModel
from models.base import Base

class Article(BaseModel, Base):
    __tablename__ = "articles"

    title = mapped_column(String(300), nullable=False)
    description = mapped_column(String(300), nullable=True)
    thumbnail = mapped_column(String(300), nullable=True)
    content = mapped_column(TEXT, nullable=False)
    source_id = mapped_column(ForeignKey("users.id"), nullable=False)
    course_id = mapped_column(ForeignKey("courses.id"), nullable=False)
    
    