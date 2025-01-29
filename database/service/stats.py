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


async def get_users_stats() -> tuple[int, int]:
    """Возвращает количество пользователей и заблокированных пользователей"""
    query = Users.select(
        fn.COUNT(Users.id).alias("count"),
        fn.SUM(Case(Users.is_banned, [(True, 1)], 0)).alias("banned_count")
    )
    return query.dicts().get()


async def get_profile_stats() -> dict:
    """Возвращает количество: пользовательских анкет,
    анкет парне, анкет девушек, не активныханкет"""
    query = Profile.select(
        fn.COUNT(Profile.user_id).alias("count"),
        fn.SUM(Case(None, [(Profile.gender == "male", 1)], 0)).alias("male_count"),
        fn.SUM(Case(None, [(Profile.gender == "female", 1)], 0)).alias("female_count"),
        fn.SUM(Case(None, [(Profile.is_active == False, 1)], 0)).alias("inactive_profile"),
    )
    return query.dicts().get()
