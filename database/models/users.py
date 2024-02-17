from peewee import TextField, IntegerField, Model, CharField, BigIntegerField
from ..connect import db, BaseModel


class Users (BaseModel):
   id=BigIntegerField(primary_key=True)
   name=CharField(max_length=50)
   gender = CharField(choices=['male', 'female'])
   find_gender = CharField(choices=['male', 'female', 'all'])
   city=CharField(max_length=50)
   photo=TextField()
   age=IntegerField()
   description=CharField(max_length=1000)

db.create_tables([Users])