"""MODULE Documentation"""
import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, scoped_session

from models.base import Base

# Make sure every ORM mapped model is imported here
# before calling Base.metadata.create_all()
from models.user import User
from models.bridge import Bridge
from models.article import Article
from models.video import Video
from models.static.image import ImageStatic
from models.static.video import VideoStatic
from models.admin.youtube import YoutubeCredentials
DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING")
DEVELOPMENT = os.getenv("ENVIRONMENT", "production").lower() == 'development'  # True or False



class DBStorage:
    """CLASS Documentation here"""
    
    __engine = None
    __session = None

    def __init__(self) -> None:
        self.__engine = create_engine(DB_CONNECTION_STRING, echo=True)
        self.reload()

    def drop_tables(self):
        """
            !!!!!!!!!
                Dangerous Area, Do not use this method in production
            !!!!!!!!!
        """
        if DEVELOPMENT:
            Base.metadata.drop_all(self.__engine)
        else:
            raise Exception("SafeGuard: Do not try to drop tables randomly in production!!!!")

    def reload(self) -> None:
        Base.metadata.create_all(self.__engine)
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
        return [obj for obj in self.__session.scalars(select(cls).filter_by(**filters))]

    def save(self) -> None:
        try:
            self.__session.commit()
        except Exception as e:
            print("Exception Occured When Saving To DataBase", e)
            self.__session.rollback

    def refresh(self, obj) -> None:
        self.__session.refresh(obj)

    def close(self) -> None:
        """Closes the Session object:: The
        connection to the database is hereby closed"""
        self.__session.close()

