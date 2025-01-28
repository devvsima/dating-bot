from peewee import TextField, IntegerField, CharField, FloatField, BooleanField, ForeignKeyField
from ..connect import BaseModel
from .users import Users

class Profile(BaseModel):
   user_id = ForeignKeyField(Users, backref='profile', primary_key=True)
   name = CharField(max_length=50)
   gender = CharField(choices=['male', 'female'], index=True)
   find_gender = CharField(choices=['male', 'female', 'all'], index=True)
   city = CharField(max_length=50)
   latitude = FloatField()
   longitude = FloatField()
   photo = TextField()
   age = IntegerField(index=True)
   description = CharField(max_length=1000)
   is_active = BooleanField(default=True, index=True)

