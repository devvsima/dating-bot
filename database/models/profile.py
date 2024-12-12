from peewee import TextField, IntegerField, Model, CharField, BigIntegerField, FloatField, BooleanField, ForeignKeyField
from ..connect import db, BaseModel
from .users import Users

class Profile(BaseModel):
   user_id = ForeignKeyField(Users, primary_key=True)
   name = CharField(max_length=50)
   gender = CharField(choices=['male', 'female'])
   find_gender = CharField(choices=['male', 'female', 'all'])
   city= CharField(max_length=50)
   latitude = FloatField()
   longitude = FloatField()
   photo = TextField()
   age = IntegerField()
   description = CharField(max_length=1000)
   active = BooleanField(default=True)

