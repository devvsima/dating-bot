import random

from loguru import logger
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from data.config import (
    AGE_RANGE,
    BLOCK_SIZE,
    INITIAL_DISTANCE,
    MAX_DISTANCE,
    MIN_PROFILES,
    RADIUS,
    RADIUS_STEP,
)
from database.models.profile import ProfileModel


async def search_profiles(
    session: AsyncSession,
    profile: ProfileModel,
) -> list:
    """
    Динамический поиск анкет: начинаем с малого радиуса и увеличиваем, пока не найдём достаточно анкет.
    """

    found_profiles = []
    current_distance = INITIAL_DISTANCE

    while current_distance <= MAX_DISTANCE and len(found_profiles) < MIN_PROFILES:
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
            * RADIUS
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
                    ProfileModel.age.between(profile.age - AGE_RANGE, profile.age + AGE_RANGE),
                    ProfileModel.id != profile.id,
                )
            )
            .order_by(distance_expr)
        )

        result = await session.execute(stmt)
        found_profiles = result.fetchall()

        # Если анкет мало — увеличиваем радиус и пробуем снова
        current_distance += RADIUS_STEP

    # Разделение на блоки и перемешивание
    blocks = {}
    for id, dist in found_profiles:
        block_key = int(dist // BLOCK_SIZE)
        blocks.setdefault(block_key, []).append(id)

    for key in blocks:
        random.shuffle(blocks[key])

    id_list = [id for key in sorted(blocks.keys()) for id in blocks[key]]

    logger.log(
        "DATABASE",
        f"{profile.id} начал поиск анкет, результат: {id_list}, радиус: {current_distance - RADIUS_STEP} км",
    )
    return id_list
