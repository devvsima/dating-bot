from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from utils.logging import logger

from ..models.profile import ProfileModel


class Profile:
    async def get(session: AsyncSession, user_id: int):
        """Возвращает профиль пользователя"""
        return await session.get(ProfileModel, user_id)

    async def delete(session: AsyncSession, user_id: int):
        """Удаляет профиль пользователя"""
        stmt = delete(ProfileModel).where(ProfileModel.user_id == user_id)
        await session.execute(stmt)
        await session.commit()
        logger.info(f"User: {user_id} | удалил профиль")

    async def update_isactive(
        session: AsyncSession, profile: ProfileModel, is_active: bool
    ) -> None:
        """Задает профилю статус, активный/не активный"""
        profile.is_active = is_active
        await session.commit()
        logger.info(f"User: {profile.user_id} | поменял статус профиля на - {is_active}")

    async def update_photo(session: AsyncSession, profile: ProfileModel, photo: str):
        """Изменяет фотографию пользователя"""
        profile.photo = photo
        await session.commit()
        logger.info(f"User: {profile.user_id} | изменил фотографию")

    async def update_description(session: AsyncSession, profile: ProfileModel, description: str):
        """Изменяет описание пользователя"""
        profile.description = description
        await session.commit()
        logger.info(f"User | {profile.user_id} изменил описание")

    async def create(
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
        if await Profile.get(session, user_id):
            await Profile.delete(session, user_id)

        profile = ProfileModel(
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
