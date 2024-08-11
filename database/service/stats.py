from ..models.users import Users
from utils.logging import logger
from peewee import fn


def get_users_invite():
    top_users = (Users
                .select(Users.id, Users.username, Users.referral)
                .order_by(Users.referral.desc())
                .limit(10))
    users = [user.username for user in top_users]
    invites = [user.referral for user in top_users]
    return users, invites
