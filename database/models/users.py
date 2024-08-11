from peewee import CharField, BigIntegerField, DateTimeField, IntegerField, BooleanField
from datetime import datetime
from ..connect import db, BaseModel


class Users(BaseModel):
   id=BigIntegerField(primary_key=True)
   username = CharField(default=None, null=True)
   language = CharField(default='en')
   role=CharField(default='user')
   referral=IntegerField(default=0)
   is_invited=BooleanField(default=False)
   created_at = DateTimeField(default=lambda: datetime.utcnow())


