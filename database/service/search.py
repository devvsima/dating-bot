from math import radians, sin, cos, sqrt, atan2
from peewee import fn
from loguru import logger
from database.models import Profile  # Убедись, что у тебя правильно импортирован Profile
from database.service.profile import get_profile  # Функция получения профиля пользователя

async def elastic_search_user_ids(user_id: int, age_range: int = 3, max_distance: float = 10) -> list:
    """
    Ищет подходящие анкеты и возвращает список id пользователей,
    отсортированных от ближайших к дальним.
    """
    profile: Profile = await get_profile(user_id)  # Получаем профиль пользователя

    # Haversine formula (расчёт расстояния через SQL)
    distance_expr = (
        fn.ACOS(
            fn.SIN(fn.RADIANS(profile.latitude)) * fn.SIN(fn.RADIANS(Profile.latitude)) +
            fn.COS(fn.RADIANS(profile.latitude)) * fn.COS(fn.RADIANS(Profile.latitude)) *
            fn.COS(fn.RADIANS(Profile.longitude - profile.longitude))
        ) * 6371  # 6371 — радиус Земли в километрах
    ).alias("distance")

    query = (
        Profile
        .select(Profile.user_id, distance_expr)
        .where(
            (Profile.is_active == True) &
            ((Profile.gender == profile.find_gender) | (profile.find_gender == "all")) &
            ((profile.gender == Profile.find_gender) | (Profile.find_gender == "all")) &
            (Profile.age.between(profile.age - age_range, profile.age + age_range)) &
            (Profile.user_id != user_id) &
            (distance_expr <= max_distance)  # Перенесли в WHERE
        )
        .order_by(distance_expr)  # Сортировка от ближнего к дальнему
    )

    return [row.user_id.id for row in query]