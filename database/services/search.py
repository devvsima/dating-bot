from loguru import logger
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.profile import ProfileModel


async def search_profiles(
    session: AsyncSession, profile: ProfileModel, age_range: int = 3, distance: float = 0.1
) -> list:
    """
    Ищет подходящие анкеты для пользователя и возвращает список id пользователей,
    которые подходят под критерии поиска.
    Поиск идет по координатам и параметрам анкеты.
    """
    # Вычисляем расстояние по координатам
    distance_expr = func.sqrt(
        func.pow(ProfileModel.latitude - profile.latitude, 2)
        + func.pow(ProfileModel.longitude - profile.longitude, 2)
    )

    stmt = (
        select(ProfileModel.user_id)
        .where(
            and_(
                ProfileModel.is_active == True,
                func.abs(ProfileModel.latitude - profile.latitude) < distance,
                func.abs(ProfileModel.longitude - profile.longitude) < distance,
                or_(ProfileModel.gender == profile.find_gender, profile.find_gender == "all"),
                or_(profile.gender == ProfileModel.find_gender, ProfileModel.find_gender == "all"),
                ProfileModel.age.between(profile.age - age_range, profile.age + age_range),
                ProfileModel.user_id != profile.user_id,
            )
        )
        .order_by(distance_expr)
    )

    result = await session.execute(stmt)
    user_ids = [row[0] for row in result.fetchall()]

    logger.log("DATABASE", f"{profile.user_id}: начал поиск анкет")

    return user_ids
