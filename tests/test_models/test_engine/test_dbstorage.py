import pytest
from unittest import TestCase

from models.engine.dbstorage import DBStorage


"""


SAVE testing should be here
add and delete object from session testing should be here

"""

@pytest.fixture
def database():
    storage = DBStorage()
    return storage


class Test_DBStorage:

    def test_storage(self, database):
        session = database.__dict__.get('_DBStorage__session')
        engine = database.__dict__.get('_DBStorage__engine')
        assert session is not None
        assert engine is not None

    def test_development(self, database):
        pass