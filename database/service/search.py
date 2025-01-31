from peewee import fn
from loguru import logger
from database.models import Profile
from database.service.profile import get_profile


async def elastic_search_user_ids(user_id: int, age_range: int = 3, distance: float = 0.1) -> list:
    """
    Ищет подходящие анкеты для пользователя и возвращает список id пользователей,
    которые подходят под критерии поиска. 
    Поиск идет по координатам и параметрам анкеты
    """
    profile: Profile = await get_profile(user_id)

    # Вычисляем расстояние по координатам
    distance_expr = fn.SQRT(
        fn.POW(Profile.latitude - profile.latitude, 2)
        + fn.POW(Profile.longitude - profile.longitude, 2)
    )

    users = (
        Profile.select(Profile.user_id, distance_expr.alias("distance"))
        .where(
            (Profile.is_active == True)
            & (fn.ABS(Profile.latitude - profile.latitude) < distance)
            & (fn.ABS(Profile.longitude - profile.longitude) < distance)
            & ((Profile.gender == profile.find_gender) | (profile.find_gender == "all"))
            & ((profile.gender == Profile.find_gender) | (Profile.find_gender == "all"))
            & (Profile.age.between(profile.age - age_range, profile.age + age_range))
            & (Profile.user_id != user_id)
        )
        .order_by(
            fn.SQRT(
                fn.POW(Profile.latitude - profile.latitude, 2)
                + fn.POW(Profile.longitude - profile.longitude, 2)
            )
        )
    )
    logger.info(f"User: {user_id} | начал поиск анкет")

    return [i.user_id.id for i in users]
