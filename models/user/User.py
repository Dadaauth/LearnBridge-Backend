from enum import IntEnum

from sqlalchemy import String, Enum, Integer
from sqlalchemy.orm import mapped_column

from ..basemodel import Base, BaseModel
from models import storage

class User(BaseModel, Base):
    __tablename__ = 'users'
    _storage = storage

    fname = mapped_column(String(150), nullable=False)
    lname = mapped_column(String(150), nullable=False)
    email = mapped_column(String(150), nullable=False)
    department = mapped_column(Enum("ECE", "MSE", "MEE", "AAE"), nullable=False)
    level = mapped_column(Integer, nullable=False)
    phone = mapped_column(String(150), nullable=False)

    def __init__(self, **attrs: dict) -> None:
        required_keys = ["fname", "lname", "email", "department", "level", "phone"]
        for key in required_keys:
            if key not in attrs:
                raise TypeError(f"Missing required keyword argument {key}")
        if attrs.get("department") not in ["ECE", "MSE", "MEE", "AAE"]:
            msg = ' or '.join(["ECE", "MSE", "MEE", "AAE"])
            raise ValueError(f"department should be either {msg}, received {attrs.get("department")}")
        if attrs.get("level") not in [100, 200, 300, 400, 500, 600, 700]:
            msg = ' or '.join(["100", "200", "300", "400", "500", "600", "700"])
            raise ValueError(f"level should be either {msg}, received {attrs.get("level")}")
        [self.__setattr__(name, val) for name, val in attrs.items()]
        # Add object to the database session
        super().add()