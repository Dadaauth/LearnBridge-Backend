"""MODULE Documentation"""
import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, scoped_session

DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING")
DEVELOPMENT = os.getenv("ENVIRONMENT", "production").lower() == 'development'  # True or False

class DBStorage:
    """CLASS Documentation here"""
    
    __engine = None
    __session = None

    def __init__(self) -> None:
        self.__engine = create_engine(DB_CONNECTION_STRING, echo=True)
        self.create_tables()
        self.load_session()

    def create_tables(self):
        from ..basemodel import Base
        Base.metadata.create_all(self.__engine)

    def drop_tables(self):
        """
            !!!!!!!!!
                Dangerous Area, Do not use this method in production
            !!!!!!!!!
        """
        from ..basemodel import Base
        if DEVELOPMENT:
            Base.metadata.drop_all(self.__engine)
        else:
            raise Exception("SafeGuard: Do not try to drop tables randomly in production!!!!")

    def load_session(self) -> None:
        session = sessionmaker(bind=self.__engine)
        Session = scoped_session(session)
        self.__session = Session()

    def new(self, obj):
        self.__session.add(obj)

    def delete(self, obj):
        self.__session.delete(obj)

    def all(self, cls):
        return [obj for obj in self.__session.scalars(select(cls)).all()]
    
    def search(self, cls, **filters):
        return [obj for obj in self.__session.scalars(select(cls).filter_by(filters))]

    def save(self) -> None:
        try:
            self.__session.commit()
        except Exception as e:
            print("Exception Occured When Saving To DataBase", e)
            self.__session.rollback
        finally:
            # Session can be re-used even after being closed.
            self.__session.close()

