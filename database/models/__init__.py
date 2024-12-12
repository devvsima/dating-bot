from .users import Users
from .profile import Profile
from .likes import Likes
from ..connect import db

db.create_tables([Users, Profile, Likes])
