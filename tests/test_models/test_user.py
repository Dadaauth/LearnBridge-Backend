from datetime import datetime, timezone
import copy
from time import sleep

import pytest
from sqlalchemy import inspect

from models.user import User
from models import storage


wrong_arguments_passed = [
    (User, {"fname": "Testing",
            "lname": "Summon",
            "email": "testing@database.com",
            "department": 20,
            "level": 100,
            "phone": "+92037264822",
            "password": "password"}),
    (User, {"fname": "Testing",
            "lname": "Summon",
            "email": "testing@database.com",
            "department": "ECE",
            "level": "100",
            "phone": "+92037264822",
            "password": "password"}),
]

incomplete_arguments_passed = [
    (User, {"fname": "Testing",
            "lname": "Summon",
            "email": "testing@database.com",
            "department": 20,
            "level": 100,
            "password": "password"}),
    (User, {"fname": "Testing",
            "lname": "Summon",
            "email": "testing@database.com",
            "department": 20,
            "phone": "+92037264822",
            "password": "password"}),
    (User, {"fname": "Testing",
            "lname": "Summon",
            "email": "testing@database.com",
            "level": 100,
            "phone": "+92037264822",
            "password": "password"}),
    (User, {"fname": "Testing",
            "lname": "Summon",
            "department": 20,
            "level": 100,
            "phone": "+92037264822",
            "password": "password"}),
    (User, {"fname": "Testing",
            "email": "testing@database.com",
            "department": 20,
            "level": 100,
            "phone": "+92037264822",
            "password": "password"}),
    (User, {
            "lname": "Summon",
            "email": "testing@database.com",
            "department": 20,
            "level": 100,
            "phone": "+92037264822",
            "password": "password"}),
    (User, {"fname": "Testing",
            "lname": "Summon",
            "email": "testing@database.com",
            "department": "ECE",
            "level": 100,
            "phone": "+92037264822"})
]

class TestUser:
    def setup_class(self):
        self.valid_user = User(
            fname="Testing",
            lname="Summon",
            email="testing@database.com",
            department="ECE",
            level=100,
            phone="+92037264822",
            password="password"
        )
        self.valid_user.save()

    def teardown_class(self):
        storage.close()
        storage.drop_tables()

    @pytest.mark.parametrize("func,attrs", incomplete_arguments_passed)
    def test_required_attrs(self, func, attrs):
        with pytest.raises(TypeError):
            func(**attrs)

    @pytest.mark.parametrize("func,attrs", wrong_arguments_passed)
    def test_required_values(self, func, attrs):
        with pytest.raises(ValueError):
            func(**attrs)

    def test_method__all(self):
        assert type(self.valid_user.all()) == list

    def test_add(self):
        insp = inspect(self.valid_user)
        assert insp.transient is False

    def test_pasword_pop(self):
        assert "password" not in self.valid_user.to_dict().keys()

    def test_to_dict(self):
        dct = copy.deepcopy(self.valid_user.__dict__)
        del dct['_sa_instance_state']
        assert self.valid_user.to_dict(pop=False) == dct

    def test_attributes_update(self):
        prev = self.valid_user.updated_at
        sleep(1)
        self.valid_user.name = "A new name"
        self.valid_user.save()
        assert self.valid_user.updated_at != prev
