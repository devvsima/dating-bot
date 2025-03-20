from loguru import logger
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.profile import ProfileModel


async def search_profiles(
    session: AsyncSession,
    profile: ProfileModel,
    age_range: int = 4,
    distance: float = 200.0,  # Радиус поиска анкет
    radius: int = 6371,  # Радиус Земли в километрах
) -> list:
    """
    Ищет подходящие анкеты для пользователя и возвращает список id пользователей,
    которые подходят под критерии поиска.
    Поиск идет по координатам и параметрам анкеты.
    """

    # Расчет расстояния с ограничением значений для функции acos
    distance_expr = (
        func.acos(
            func.greatest(
                func.least(
                    func.cos(func.radians(profile.latitude))
                    * func.cos(func.radians(ProfileModel.latitude))
                    * func.cos(
                        func.radians(ProfileModel.longitude) - func.radians(profile.longitude)
                    )
                    + func.sin(func.radians(profile.latitude))
                    * func.sin(func.radians(ProfileModel.latitude)),
                    1.0,  # Ограничение сверху
                ),
                -1.0,  # Ограничение снизу
            )
        )
        * radius
    )

    stmt = (
        select(ProfileModel.user_id)
        .where(
            and_(
                ProfileModel.is_active == True,
                distance_expr < distance,  # Ограничение по радиусу (200 км)
                or_(ProfileModel.gender == profile.find_gender, profile.find_gender == "all"),
                or_(profile.gender == ProfileModel.find_gender, ProfileModel.find_gender == "all"),
                ProfileModel.age.between(profile.age - age_range, profile.age + age_range),
                ProfileModel.user_id != profile.user_id,
            )
        )
        .order_by(distance_expr)
    )

    result = await session.execute(stmt)
    id_list = [row[0] for row in result.fetchall()]

    logger.log("DATABASE", f"{profile.user_id} начал поиск анкет, результат: {id_list}")
    return id_list
