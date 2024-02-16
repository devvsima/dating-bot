from peewee import TextField, IntegerField, Model, CharField
from ..connect import db


class BaseModel(Model):
    class Meta:
        database = db


class Users (BaseModel):
   id=IntegerField(primary_key=True)
   name=CharField(max_length=50)
   gender = CharField(choices=['male', 'female'])
   find_gender = CharField(choices=['male', 'female', 'all'])
   city=CharField(max_length=50)
   photo=TextField()
   age=IntegerField()
   description=CharField(max_length=1000)
