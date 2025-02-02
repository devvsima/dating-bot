from peewee import ForeignKeyField
from ..connect import BaseModel

from .users import Users


class Likes(BaseModel):
    liker_id = ForeignKeyField(Users, backref="likes_given")
    liked_id = ForeignKeyField(Users, backref="likes_received")
