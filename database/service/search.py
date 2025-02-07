from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from database.models.profile import Profile
from database.service.profiles import get_profile


async def elastic_search_user_ids(
    session: AsyncSession, user_id: int, age_range: int = 3, distance: float = 0.1
) -> list:
    """
    Ищет подходящие анкеты для пользователя и возвращает список id пользователей,
    которые подходят под критерии поиска.
    Поиск идет по координатам и параметрам анкеты.
    """
    profile: Profile = await get_profile(session, user_id)
    if not profile:
        return []

    # Вычисляем расстояние по координатам
    distance_expr = func.sqrt(
        func.pow(Profile.latitude - profile.latitude, 2)
        + func.pow(Profile.longitude - profile.longitude, 2)
    )

    stmt = (
        select(Profile.user_id)
        .where(
            and_(
                Profile.is_active == True,
                func.abs(Profile.latitude - profile.latitude) < distance,
                func.abs(Profile.longitude - profile.longitude) < distance,
                or_(Profile.gender == profile.find_gender, profile.find_gender == "all"),
                or_(profile.gender == Profile.find_gender, Profile.find_gender == "all"),
                Profile.age.between(profile.age - age_range, profile.age + age_range),
                Profile.user_id != user_id,
            )
        )
        .order_by(distance_expr)
    )

    result = await session.execute(stmt)
    user_ids = [row[0] for row in result.fetchall()]

    logger.info(f"User: {user_id} | начал поиск анкет")

    return user_ids
