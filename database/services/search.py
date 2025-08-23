import math
import random

from loguru import logger
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from data.config import search
from database.models.profile import ProfileModel


def calculate_age_range(age: int) -> int:
    """
    Вычисляет динамический возрастной диапазон на основе возраста пользователя.

    Формула: max(MIN_AGE_RANGE, возраст * AGE_RANGE_MULTIPLIER)
    Ограничения: минимум MIN_AGE_RANGE лет, максимум MAX_AGE_RANGE лет

    Примеры:
    - 16 лет → 3 года
    - 25 лет → 4 года
    - 30 лет → 5 лет
    - 50 лет → 8 лет
    - 60+ лет → 15 лет (максимум)
    """
    calculated_range = max(search.MIN_AGE_RANGE, age * search.AGE_RANGE_MULTIPLIER)
    return min(search.MAX_AGE_RANGE, round(calculated_range))


async def search_profiles(
    session: AsyncSession,
    profile: ProfileModel,
) -> list:
    """
    Динамический поиск анкет: начинаем с малого радиуса и увеличиваем, пока не найдём достаточно анкет.
    Использует умный расчет возрастного диапазона.
    """

    # Проверяем, что профиль существует и имеет необходимые данные
    if not profile:
        return []

    if not profile.latitude or not profile.longitude:
        return []

    # Вычисляем динамический возрастной диапазон
    dynamic_age_range = calculate_age_range(profile.age)

    logger.log(
        "DATABASE",
        f"User {profile.id} (age {profile.age}): using age range ±{dynamic_age_range} years",
    )

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
                    # Используем динамический возрастной диапазон
                    ProfileModel.age.between(
                        profile.age - dynamic_age_range, profile.age + dynamic_age_range
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
        f"User {profile.id} (age {profile.age}, ±{dynamic_age_range} years) found {len(id_list)} profiles within {current_distance - search.RADIUS_STEP} km",
    )
    return id_list


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
