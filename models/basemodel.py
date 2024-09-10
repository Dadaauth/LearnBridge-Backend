from datetime import datetime, timezone
from typing import Any, Optional, List
from uuid import uuid4
import copy

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column

import models
from lib.error import Error

class BaseModel:
    """
    Class:
        BaseModel: The base class most models will inherit from.
            It contains most of the methods needed by each database models

        :methods
            delete: Deletes an object from the current session
            add: adds an object to the current database session
            save: persist the object details in the database
    """
    
    id = mapped_column(String(60), default=str(uuid4()),  primary_key=True, nullable=False)
    created_at = mapped_column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = mapped_column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    def __init__(self) -> None:
        self.id = str(uuid4())
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def update(self, **kwargs: dict) -> None:
        """
            Update a set of attributes in an object.
            :params
                @kwargs: a dictionary of attributes
                        to update
        """
        {setattr(self, key, value) for key, value in kwargs.items()}

    def check_required_keys(self, required_keys: list, **kwargs: dict) -> bool:
        """
            Checks if the named arguments required by the class
            are provided accurately
            :params
                @required_keys: a list of required keys
                @kwargs: a dictionary containing the keys
                    to be tested
        """
        for key in required_keys:
            if key not in kwargs:
                return Error(1001, "Required key(s) not present")
        return True

    def delete(self) -> None:
        """
            :method
                delete: deletes or removes an object from the session.
                        The object row will be deleted from the database
                        on the next commit or whenever the :method save is
                        called with the delete argument
        """
        models.storage.delete(self)

    def add(self) -> None:
        """
            :method
                add: j
        """
        models.storage.new(self)

    def save(self, delete=False) -> None:
        if not delete:
            self.updated_at = datetime.now(timezone.utc)
            models.storage.new(self)
        return models.storage.save()

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
