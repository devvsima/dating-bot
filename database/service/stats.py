from utils.logging import logger

from ..models.users import Users
from ..models.profile import Profile

from peewee import fn, Case

def get_users_invite() -> list:
    top_users = (Users
                .select(Users.id, Users.username, Users.referral)
                .order_by(Users.referral.desc())
                .limit(5))
    users = [user.username for user in top_users]
    invites = [user.referral for user in top_users]
    return users, invites


def get_users_registration_data() -> list:
    users = (Users
                .select(Users.id, Users.username, Users.created_at)
                .order_by(Users.referral.desc()))
    # Формируем данные в виде списка словарей
    registration_data = [{"username": user.username, "timestamp": user.created_at}  for user in users]
    return registration_data


def get_users_stats() -> int:
    return Users.select().count()

def get_profile_stats() -> dict:
    query = Profile.select(
    fn.COUNT(Profile.id).alias('total_users'),
    fn.SUM(Case(None, [(Profile.gender == 'male', 1)], 0)).alias('male_users'),
    fn.SUM(Case(None, [(Profile.gender == 'female', 1)], 0)).alias('female_users')
    )
    return query.dicts().get()
