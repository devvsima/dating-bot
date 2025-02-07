from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.profile import Profile
from utils.logging import logger


async def get_profile(session: AsyncSession, user_id: int):
    """Возвращает профиль пользователя"""
    return await session.get(Profile, user_id)


async def get_profile_with_user(session: AsyncSession, user_id: int):
    """Возвращает профиль пользователя с данными пользователя"""
    stmt = select(Profile).options(joinedload(Profile.user)).where(Profile.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def delete_profile(session: AsyncSession, user_id: int):
    """Удаляет профиль пользователя"""
    stmt = delete(Profile).where(Profile.user_id == user_id)
    await session.execute(stmt)
    await session.commit()
    logger.info(f"User: {user_id} | удалил профиль")


async def update_profile_is_active_status(
    session: AsyncSession, user_id: int, is_active: bool
) -> None:
    """Задает профилю статус, активный/не активный"""
    await session.execute(
        update(Profile).where(Profile.user_id == user_id).values(is_active=is_active)
    )
    await session.commit()
    logger.info(f"User: {user_id} | поменял статус профиля на - {is_active}")


async def edit_profile_photo(session: AsyncSession, user_id: int, photo: str):
    """Изменяет фотографию пользователя"""
    await session.execute(update(Profile).where(Profile.user_id == user_id).values(photo=photo))
    await session.commit()
    logger.info(f"User: {user_id} | изменил фотографию")


async def edit_profile_description(session: AsyncSession, user_id: int, description: str):
    """Изменяет описание пользователя"""

    await session.execute(
        update(Profile).where(Profile.user_id == user_id).values(description=description)
    )
    await session.commit()
    logger.info(f"User | {user_id} изменил описание")


async def create_profile(
    session: AsyncSession,
    user_id: int,
    gender: str,
    find_gender: str,
    photo: str,
    name: str,
    age: int,
    city: str,
    latitude: str,
    longitude: str,
    description: str,
):
    """Создает профиль пользователя, если профиль есть - удаляет его"""
    if await get_profile(session, user_id):
        await delete_profile(session, user_id)

    profile = Profile(
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

    session.add(profile)
    await session.commit()
    logger.info(f"User: {user_id} | создал анкету")
