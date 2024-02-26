from .users import Users
from .profile import Profile
from ..connect import db

db.create_tables([Profile, Users])
