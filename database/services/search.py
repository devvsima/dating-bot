import math
import random
import time

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from data.config import search
from database.models.profile import ProfileModel
from utils.logging import logger


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> int:
    """
    Возвращает примерное расстояние между двумя точками (в километрах)
    по координатам широты и долготы.
    """
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(search.EARTH_RADIUS * c)


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
    initial_distance: float = search.INITIAL_DISTANCE,
    max_distance: float = search.MAX_DISTANCE,
    radius_step: float = search.RADIUS_STEP,
    min_profiles: int = search.MIN_PROFILES,
    block_size: float = search.BLOCK_SIZE,
    earth_radius: int = search.EARTH_RADIUS,
    force_shuffle: bool = True,
) -> list:
    """
    Динамический поиск анкет: начинаем с малого радиуса и увеличиваем, пока не найдём достаточно анкет.
    Использует умный расчет возрастного диапазона и блочное перемешивание.

    Args:
        session: Сессия базы данных
        profile: Профиль пользователя для поиска
        initial_distance: Начальная дистанция поиска (км)
        max_distance: Максимальная дистанция поиска (км)
        radius_step: Шаг увеличения радиуса (км)
        min_profiles: Минимальное количество профилей для поиска
        block_size: Размер блока для перемешивания (км)
        earth_radius: Радиус Земли в км
        force_shuffle: Принудительное перемешивание при каждом вызове
    """

    # Проверяем, что профиль существует и имеет необходимые данные
    if not profile:
        return []

    if not profile.latitude or not profile.longitude:
        return []

    # Используем переданные параметры или значения по умолчанию из конфига
    initial_distance = initial_distance or search.INITIAL_DISTANCE
    max_distance = max_distance or search.MAX_DISTANCE
    radius_step = radius_step or search.RADIUS_STEP
    min_profiles = min_profiles or search.MIN_PROFILES
    block_size = block_size or search.BLOCK_SIZE
    earth_radius = earth_radius or search.RADIUS

    # Вычисляем динамический возрастной диапазон
    dynamic_age_range = calculate_age_range(profile.age)

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
            * earth_radius
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
        current_distance += radius_step

    # Разделение на блоки и перемешивание
    blocks = {}
    for id, dist in found_profiles:
        block_key = int(dist // block_size)
        blocks.setdefault(block_key, []).append(id)

    # Перемешиваем профили внутри каждого блока
    if force_shuffle:
        random.seed(int(time.time() * 1000000) % 2147483647)

    for key in blocks:
        random.shuffle(blocks[key])

    # Собираем отсортированный по блокам список с перемешанным содержимым
    id_list = [id for key in sorted(blocks.keys()) for id in blocks[key]]

    logger.log(
        "DATABASE",
        f"User {profile.id} (age {profile.age}, ±{dynamic_age_range} years) found {len(id_list)} profiles "
        f"in radius {current_distance - radius_step:.1f}km, shuffled={'Yes' if force_shuffle else 'No'}",
    )

    return id_list
