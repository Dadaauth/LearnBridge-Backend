
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.mysql import TEXT

from models.basemodel import BaseModel
from models.base import Base

class YoutubeCredentials(BaseModel, Base):
    __tablename__ = "youtube_credentials"

    token = mapped_column(String(500), nullable=False)
    refresh_token = mapped_column(String(500), nullable=False)
    token_uri = mapped_column(String(500), nullable=False)
    client_id = mapped_column(String(500), nullable=False)
    client_secret = mapped_column(String(500), nullable=False)
    scopes = mapped_column(TEXT, nullable=False)

    def __init__(self, **kwargs):
        super().__init__()
        required_keys = ["token", "refresh_token", "scopes", "token_uri", "client_id", "client_secret"]
        for key in required_keys:
            if key not in kwargs:
                raise KeyError
        scopes = kwargs["scopes"]
        scopes_str = ""
        for scope in scopes:
            scopes_str += scope
            scopes_str += " "
        kwargs["scopes"] = scopes_str
        [setattr(self, key, val) for key, val in kwargs.items()]
