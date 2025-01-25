from peewee import fn

from ..models.profile import Profile

from .profile import get_profile

from utils.logging import logger


async def elastic_search_user_ids(user_id: int, age_range: int = 3, distance: float = 0.1) -> list:
    """
    Возвращает список id пользователей, которые подходят под критерии поиска,
    поиск идет по координатам
    """
    user = await get_profile(user_id)

    # Вычисляем расстояние по координатам
    distance_expr = fn.SQRT(
        fn.POW(Profile.latitude - user.latitude, 2)
        + fn.POW(Profile.longitude - user.longitude, 2)
    )

    users = (
        Profile.select(Profile.user_id, distance_expr.alias("distance"))
        .where(
            (Profile.active == True)
            & (fn.ABS(Profile.latitude - user.latitude) < distance)
            & (fn.ABS(Profile.longitude - user.longitude) < distance)
            & ((Profile.gender == user.find_gender) | (user.find_gender == "all"))
            & ((user.gender == Profile.find_gender) | (Profile.find_gender == "all"))
            & (Profile.age.between(user.age - age_range, user.age + age_range))
            & (Profile.user_id != user_id)
        )
        .order_by(
            fn.SQRT(
                fn.POW(Profile.latitude - user.latitude, 2)
                + fn.POW(Profile.longitude - user.longitude, 2)
            )
        )
    )
    logger.info(f"User: {user_id} | начал поиск анкет")

    return [i.user_id for i in users]
