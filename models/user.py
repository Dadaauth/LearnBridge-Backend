from sqlalchemy import String, Enum, Integer, ForeignKey, Date
from sqlalchemy.orm import mapped_column, relationship

from flask_bcrypt import generate_password_hash

from models.basemodel import BaseModel
from models.base import Base

class User(BaseModel, Base):
    __tablename__ = 'users'

    first_name = mapped_column(String(300), nullable=False)
    last_name = mapped_column(String(300), nullable=False)
    email = mapped_column(String(300), nullable=False)
    level = mapped_column(Integer, nullable=False)
    department = mapped_column(String(300), nullable=False)
    faculty = mapped_column(String(300), nullable=False)
    dob = mapped_column(Date, nullable=False)
    phone_calls = mapped_column(String(45), nullable=False)
    phone_whatsapp = mapped_column(String(45), nullable=True)
