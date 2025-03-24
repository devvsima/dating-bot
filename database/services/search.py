import random

from loguru import logger
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.profile import ProfileModel

age_range: int = 4
initial_distance: float = 200.0  # Стартовый радиус
max_distance: float = 10000.0  # Максимальный радиус
radius_step: float = 200.0  # Шаг увеличения радиуса
min_profiles: int = 100  # Минимальное количество анкет
radius: int = 6371  # Радиус Земли
block_size: float = 50.0  # Размер блока для перемешивания


async def search_profiles(
    session: AsyncSession,
    profile: ProfileModel,
) -> list:
    """
    Динамический поиск анкет: начинаем с малого радиуса и увеличиваем, пока не найдём достаточно анкет.
    """

    found_profiles = []
    current_distance = initial_distance

    while current_distance <= max_distance and len(found_profiles) < min_profiles:
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
            * radius
        )

        stmt = (
            select(ProfileModel.user_id, distance_expr.label("distance"))
            .where(
                and_(
                    ProfileModel.is_active == True,
                    distance_expr < current_distance,
                    or_(ProfileModel.gender == profile.find_gender, profile.find_gender == "all"),
                    or_(
                        profile.gender == ProfileModel.find_gender,
                        ProfileModel.find_gender == "all",
                    ),
                    ProfileModel.age.between(profile.age - age_range, profile.age + age_range),
                    ProfileModel.user_id != profile.user_id,
                )
            )
            .order_by(distance_expr)
        )

        result = await session.execute(stmt)
        found_profiles = result.fetchall()

        # Если анкет мало — увеличиваем радиус и пробуем снова
        current_distance += radius_step

    # Разделение на блоки и перемешивание
    blocks = {}
    for user_id, dist in found_profiles:
        block_key = int(dist // block_size)
        blocks.setdefault(block_key, []).append(user_id)

    for key in blocks:
        random.shuffle(blocks[key])

    id_list = [user_id for key in sorted(blocks.keys()) for user_id in blocks[key]]

    logger.log(
        "DATABASE",
        f"{profile.user_id} начал поиск анкет, результат: {id_list}, радиус: {current_distance - radius_step} км",
    )
    return id_list
