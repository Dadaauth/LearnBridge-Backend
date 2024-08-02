from datetime import datetime, timezone
from typing import Any, Optional, List
from uuid import uuid4
import copy

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column

import models

class BaseModel:
    
    id = mapped_column(String(150), default=str(uuid4()),  primary_key=True, nullable=False)
    created_at = mapped_column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = mapped_column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    def __init__(self) -> None:
        pass

    def delete(self) -> None:
        models.storage.delete(self)

    def add(self) -> None:
        models.storage.new(self)

    def save(self) -> None:
        self.updated_at = datetime.now(timezone.utc)
        models.storage.new(self)
        models.storage.save()

    def refresh(self):
        models.storage.refresh(self)

    @classmethod
    def all(cls):
        return models.storage.all(cls)
    
    @classmethod
    def search(cls, **filters: dict) -> list:
        return models.storage.search(cls, **filters)
    
    def to_dict(self, strip: Optional[List[str]] = None) -> dict:
        dict_repr = copy.deepcopy(self.__dict__)
        if '_sa_instance_state' in dict_repr:
            del dict_repr['_sa_instance_state']
        if strip is not None:
            return {key: value for key, value in dict_repr.items() if key not in strip}
        return dict_repr

    def __repr__(self) -> str:
        attrs = ", ".join([f"{key}={value}" for key, value in self.__dict__.items()])
        return f"{self.__class__.__name__}({attrs})"
