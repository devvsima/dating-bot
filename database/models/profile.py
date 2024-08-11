from peewee import TextField, IntegerField, Model, CharField, BigIntegerField, FloatField, BooleanField
from ..connect import db, BaseModel

class Profile(BaseModel):
   id = BigIntegerField(primary_key=True)
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

