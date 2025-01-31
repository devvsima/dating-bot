from ..models.profile import Profile

from utils.logging import logger


async def get_profile(user_id: int):
    """Возвращает профиль пользователя"""
    return Profile.get_or_none(Profile.user_id == user_id)


async def delete_profile(user_id: int):
    """Удаляет профиль пользователя"""
    Profile.delete().where(Profile.user_id == user_id).execute()
    logger.info(f"User: {user_id} | удалил профиль")


async def update_profile_is_active_status(user_id: int, is_active: bool) -> None:
    """Задает профилю статус, активны/не активный"""
    Profile.update(is_active=is_active).where(Profile.user_id == user_id).execute()
    logger.info(f"User: {user_id} | поменял стату профиля на - {is_active}")


async def edit_profile_photo(user_id, photo):
    """Изменяет фотографию пользователя"""
    Profile.update(photo=photo).where(Profile.user_id == user_id).execute()
    logger.info(f"User: {user_id} | изменил фотографию")


async def edit_profile_description(user_id, description):
    """Изменяет описание пользователя"""
    Profile.update(description=description).where(Profile.user_id == user_id).execute()
    logger.info(f"User | {user_id} изменил описание")


async def create_profile(
        user_id: int, gender: str, find_gender: str,
        photo: str, name: str, age: int, city: str,
        latitude: str, longitude: str, description: str,
):
    """Создает профиль пользователя, если профиль есть - удаляет его"""
    if await get_profile(user_id):
        await delete_profile(user_id)

    Profile.create(
        user_id=user_id,
        gender=gender,
        find_gender=find_gender,
        photo=photo,
        name=name,
        age=age,
        city=city,
        latitude=latitude,
        longitude=longitude,
        description=description,
    )
    logger.info(f"User: {user_id} | создал анкету")
