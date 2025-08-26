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
    initial_distance: float = search.INITIAL_DISTANCE,
    max_distance: float = search.MAX_DISTANCE,
    radius_step: float = search.RADIUS_STEP,
    min_profiles: int = search.MIN_PROFILES,
    block_size: float = search.BLOCK_SIZE,
    earth_radius: int = search.EARTH_RADIUS,
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

    logger.log(
        "DATABASE",
        f"Search parameters: initial_distance={initial_distance}km, max_distance={max_distance}km, "
        f"radius_step={radius_step}km, min_profiles={min_profiles}, block_size={block_size}km, "
        f"age_range=±{dynamic_age_range} years for user {profile.id} (age {profile.age})",
    )

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
    for key in blocks:
        random.shuffle(blocks[key])

    # Собираем отсортированный по блокам список с перемешанным содержимым
    id_list = [id for key in sorted(blocks.keys()) for id in blocks[key]]

    return id_list


def debug_shuffle_logic(found_profiles: list, block_size: float) -> dict:
    """
    Отладочная функция для анализа работы перемешивания.
    Возвращает детальную информацию о блоках.
    """
    blocks = {}
    debug_info = {
        "total_profiles": len(found_profiles),
        "block_size": block_size,
        "blocks": {},
        "shuffled_order": [],
    }

    # Разделяем на блоки
    for i, (id, dist) in enumerate(found_profiles):
        block_key = int(dist // block_size)
        blocks.setdefault(block_key, []).append((id, dist, i))

    # Подготавливаем информацию о блоках
    for block_key, profiles in blocks.items():
        debug_info["blocks"][block_key] = {
            "count": len(profiles),
            "distance_range": f"{min(p[1] for p in profiles):.1f} - {max(p[1] for p in profiles):.1f} km",
            "original_order": [p[0] for p in profiles],
            "original_positions": [p[2] for p in profiles],
        }

        # Перемешиваем
        profile_ids = [p[0] for p in profiles]
        random.shuffle(profile_ids)
        debug_info["blocks"][block_key]["shuffled_order"] = profile_ids

        # Добавляем в общий список
        debug_info["shuffled_order"].extend(profile_ids)

    logger.log(
        "DATABASE",
        f"Shuffle debug: {len(blocks)} blocks created, "
        f"total profiles: {debug_info['total_profiles']}",
    )

    return debug_info


async def search_profiles_with_debug(
    session: AsyncSession, profile: ProfileModel, debug: bool = False, **kwargs
) -> tuple[list, dict]:
    """
    Версия search_profiles с отладочной информацией.
    Возвращает (id_list, debug_info) если debug=True, иначе только id_list.
    """
    # Все те же параметры как в основной функции
    initial_distance = kwargs.get("initial_distance") or search.INITIAL_DISTANCE
    max_distance = kwargs.get("max_distance") or search.MAX_DISTANCE
    radius_step = kwargs.get("radius_step") or search.RADIUS_STEP
    min_profiles = kwargs.get("min_profiles") or search.MIN_PROFILES
    block_size = kwargs.get("block_size") or search.BLOCK_SIZE
    earth_radius = kwargs.get("earth_radius") or search.RADIUS

    # Получаем результаты поиска
    id_list = await search_profiles(session, profile, **kwargs)

    if not debug:
        return id_list, {}

    # Для отладки нужно повторить запрос и получить расстояния
    dynamic_age_range = calculate_age_range(profile.age)
    current_distance = max_distance  # Берем максимальный радиус для полного анализа

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

    debug_info = debug_shuffle_logic(found_profiles, block_size)

    return id_list, debug_info


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
