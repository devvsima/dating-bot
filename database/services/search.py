import random

from loguru import logger
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from data.config import search
from database.models.profile import ProfileModel


async def search_profiles(
    session: AsyncSession,
    profile: ProfileModel,
) -> list:
    """
    Динамический поиск анкет: начинаем с малого радиуса и увеличиваем, пока не найдём достаточно анкет.
    """

    # Проверяем, что профиль существует и имеет необходимые данные
    if not profile:
        return []

    if not profile.latitude or not profile.longitude:
        return []

    found_profiles = []
    current_distance = search.INITIAL_DISTANCE

    while current_distance <= search.MAX_DISTANCE and len(found_profiles) < search.MIN_PROFILES:
        # Расчёт расстояния
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
                        1.0,
                    ),
                    -1.0,
                )
            )
            * search.RADIUS
        )

        stmt = (
            select(ProfileModel.id, distance_expr.label("distance"))
            .where(
                and_(
                    ProfileModel.is_active == True,
                    distance_expr < current_distance,
                    or_(ProfileModel.gender == profile.find_gender, profile.find_gender == "all"),
                    or_(
                        profile.gender == ProfileModel.find_gender,
                        ProfileModel.find_gender == "all",
                    ),
                    ProfileModel.age.between(
                        profile.age - search.AGE_RANGE, profile.age + search.AGE_RANGE
                    ),
                    ProfileModel.id != profile.id,
                )
            )
            .order_by(distance_expr)
        )

        result = await session.execute(stmt)
        found_profiles = result.fetchall()

        # Если анкет мало — увеличиваем радиус и пробуем снова
        current_distance += search.RADIUS_STEP

    # Разделение на блоки и перемешивание
    blocks = {}
    for id, dist in found_profiles:
        block_key = int(dist // search.BLOCK_SIZE)
        blocks.setdefault(block_key, []).append(id)

    for key in blocks:
        random.shuffle(blocks[key])

    id_list = [id for key in sorted(blocks.keys()) for id in blocks[key]]

    logger.log(
        "DATABASE",
        f"{profile.id} начал поиск анкет, результат: {id_list}, радиус: {current_distance - search.RADIUS_STEP} км",
    )
    return id_list


import math


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Возвращает примерное расстояние между двумя точками (в километрах)
    по координатам широты и долготы.
    """
    R = 6371  # Радиус Земли в километрах
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(R * c)
