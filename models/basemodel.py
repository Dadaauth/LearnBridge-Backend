from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass

class BaseModel:
    
    id = mapped_column(String(150), default=str(uuid4()),  primary_key=True, nullable=False)
    created_at = mapped_column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = mapped_column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    def add(self) -> None:
        self._storage.new(self)

    def delete(self) -> None:
        self._storage.delete(self)

    def save(self) -> None:
        self._storage.save()

    @classmethod
    def all(cls):
        return cls._storage.all(cls)
    
    @classmethod
    def search(cls, **filters: dict) -> list:
        return cls._storage.search(cls, **filters)
    
    def to_dict(self) -> dict:
        return self.__dict__.copy()

    def __setattr__(self, key: str, value: Any) -> None:
        if key != 'updated_at':
            if key in self.__dict__ and self.__dict__[key] != value:
                self.__dict__['updated_at'] = datetime.now(timezone.utc)
                self.__dict__[key] = value
            else:
                self.__dict__['updated_at'] = datetime.now(timezone.utc)
                self.__dict__[key] = value
        else:
            self.__dict__[key] = value

    def __repr__(self) -> str:
        attrs = ", ".join([f"{key}={value}" for key, value in self.__dict__.items()])
        return f"{self.__class__.__name__}({attrs})"
