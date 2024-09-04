from peewee import ForeignKeyField, CharField
from ..connect import db, BaseModel

from .users import Users

class Likes(BaseModel):
   liker_id = ForeignKeyField(Users, backref='likes_given')
   liked_id = ForeignKeyField(Users, backref='likes_received')

