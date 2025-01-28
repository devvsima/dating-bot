from peewee import fn, Case

from typing import Any

from ..models.users import Users
from ..models.profile import Profile


async def get_all_users_registration_data() -> list:
    users = Users.select(Users.id, Users.username, Users.created_at).order_by(
        Users.referral.desc()
    )
    # Формируем данные в виде списка словарей
    registration_data = [{"username": user.username, "timestamp": user.created_at} for user in users]
    return registration_data


async def get_users_stats() -> int:
    """Возвращает количество пользователей в БД"""
    return Users.select().count()


async def get_profile_stats() -> dict:
    """Возвращает количество пользовательских анкет, мужских и женских"""
    query = Profile.select(
        fn.COUNT(Profile.user_id).alias("users_count"),
        fn.SUM(Case(None, [(Profile.gender == "male", 1)], 0)).alias("male_count"),
        fn.SUM(Case(None, [(Profile.gender == "female", 1)], 0)).alias("female_count"),
        fn.SUM(Case(None, [(Profile.is_active == True, 1)], 0)).alias("active_profile"),
    )
    return query.dicts().get()
