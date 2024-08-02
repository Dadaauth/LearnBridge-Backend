from sqlalchemy import String, Enum, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship

from flask_bcrypt import generate_password_hash

from models.basemodel import BaseModel
from models.base import Base
from errors.my_errors import MyValueError

class User(BaseModel, Base):
    __tablename__ = 'users'

    fname = mapped_column(String(150), nullable=False)
    lname = mapped_column(String(150), nullable=False)
    email = mapped_column(String(150), nullable=False, unique=True)
    department = mapped_column(Enum("ECE", "MSE", "MEE", "AAE"), nullable=False)
    level = mapped_column(Integer, nullable=False)
    phone = mapped_column(String(150), nullable=False)
    password = mapped_column(String(300), nullable=False)
    
    bridge_id = mapped_column(ForeignKey("bridges.id"))
    bridge = relationship("Bridge", back_populates="user")

    def __init__(self, **attrs: dict) -> None:
        super().__init__()
        required_keys = ["fname", "lname", "email", "department", "level", "phone", "password"]
        for key in required_keys:
            if key not in attrs:
                raise TypeError(f"Missing required keyword argument {key}")
        if attrs.get("department") not in ["ECE", "MSE", "MEE", "AAE"]:
            msg = ' or '.join(["ECE", "MSE", "MEE", "AAE"])
            raise ValueError(f"department should be either {msg}, received {attrs.get("department")}")
        attrs["level"] = int(attrs.get("level"))
        if attrs.get("level") not in [100, 200, 300, 400, 500, 600, 700]:
            msg = ' or '.join(["100", "200", "300", "400", "500", "600", "700"])
            raise ValueError(f"level should be either {msg}, received {attrs.get("level")}")
        for user in User.all():
            if user.email == attrs.get("email"):
                raise MyValueError(f"User with email {attrs.get("email")} already exists", 1001)
        # encrypt the password here
        attrs["password"] = generate_password_hash(attrs.get("password")).decode('utf-8')
        [setattr(self, name, val) if name in required_keys else "" for name, val in attrs.items()]

    def to_dict(self, pop=True) -> dict:
        if pop:
            return super().to_dict(["password"])
        else:
            return super().to_dict()