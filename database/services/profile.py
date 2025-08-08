from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.services.base import BaseService
from database.services.profile_media import ProfileMedia
from utils.logging import logger

from ..models.profile import ProfileModel


class Profile(BaseService):
    model = ProfileModel

    @staticmethod
    async def get(session: AsyncSession, id: int):
        """Возвращает профиль пользователя"""
        return await session.get(ProfileModel, id)

    @staticmethod
    async def delete(session: AsyncSession, id: int):
        """Удаляет профиль пользователя"""
        stmt = delete(ProfileModel).where(ProfileModel.id == id)
        await session.execute(stmt)
        await session.commit()
        logger.log("DATABASE", f"{id}: удалил профиль")

    @classmethod
    async def create_or_update(cls, session: AsyncSession, **kwargs):
        """Создает профиль пользователя, если профиль есть - обновляет его"""
        profile_id = kwargs.pop("id")  # Извлекаем id профиля
        photo_url = kwargs.pop(
            "photo", None
        )  # Извлекаем photo, если есть (для обратной совместимости)
        photos = kwargs.pop("photos", None)  # Извлекаем список фото

        obj = await cls.get_by_id(session, profile_id)
        is_new = False

        if obj:
            # Обновляем существующий профиль
            for key, value in kwargs.items():
                setattr(obj, key, value)
            await session.commit()
        else:
            # Создаем новый профиль
            obj = await cls.create(session, id=profile_id, **kwargs)
            is_new = True
            logger.log("DATABASE", f"{profile_id}: создал анкету")

        # Обрабатываем фото
        if photos:
            # Удаляем все старые фото профиля
            await ProfileMedia.delete_profile_photos(session, profile_id)

            # Добавляем новые фото
            for i, photo_file_id in enumerate(photos, 1):
                await ProfileMedia.add_media(
                    session=session,
                    profile_id=profile_id,
                    media_url=photo_file_id,
                    media_type="photo",
                    order=i,
                )
        elif photo_url:
            # Обратная совместимость - если передано одно фото
            await ProfileMedia.delete_profile_photos(session, profile_id)

            await ProfileMedia.add_media(
                session=session,
                profile_id=profile_id,
                media_url=photo_url,
                media_type="photo",
                order=1,
            )

        return obj, is_new
