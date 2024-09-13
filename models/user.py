from datetime import datetime

from sqlalchemy import String, Enum, Integer, ForeignKey, Date
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.mysql import MEDIUMTEXT

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
    password = mapped_column(MEDIUMTEXT, nullable=False)
    picture = mapped_column(String(300), nullable=True)


    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__()
        # Verify that all required attributes are sent to the class
        # self.check_required_keys(
        #     [""]
        # )
        [setattr(self, key, value) for key, value in kwargs.items()]
        self.password = generate_password_hash(self.password)
        self.level = int(self.level)
        self.dob = datetime.strptime(self.dob, "%Y-%m-%d")

    def basic_info(self) -> dict:
        info = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "level": self.level,
            "department": self.department,
            "faculty": self.faculty,
            "picture": self.picture,
        }
        return info

    def info(self, fields: dict) -> dict:
        info = {}
        for field in fields:
            info[field] = self.get(field)
        return info        
