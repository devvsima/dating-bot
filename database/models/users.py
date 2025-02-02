from peewee import CharField, BigIntegerField, DateTimeField, IntegerField, BooleanField
from datetime import datetime
from ..connect import BaseModel


class Users(BaseModel):
    id = BigIntegerField(primary_key=True)
    username = CharField(default=None, null=True)
    language = CharField(default="en")
    referral = IntegerField(default=0)
    is_banned = BooleanField(default=False)
    created_at = DateTimeField(default=lambda: datetime.utcnow())
