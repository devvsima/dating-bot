from peewee import BigIntegerField
from ..connect import db, BaseModel


class Likes(BaseModel):
   user_id = BigIntegerField()
   liked_profile_id = BigIntegerField()


