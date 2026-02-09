from typing import List, Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.queries.base import BaseService
from utils.logging import logger

from ..models.profile_media import ProfileMediaModel


class ProfileMedia(BaseService):
    model = ProfileMediaModel

    @staticmethod
    async def get_by_id(session: AsyncSession, id: int) -> Optional[ProfileMediaModel]:
        """Возвращает медиа по ID"""
        return await session.get(ProfileMediaModel, id)

    @staticmethod
    async def get_profile_media(
        session: AsyncSession, profile_id: int, media_type: Optional[str] = None
    ) -> List[ProfileMediaModel]:
        """Возвращает все медиа профиля, отсортированные по порядку"""
        stmt = select(ProfileMediaModel).where(ProfileMediaModel.profile_id == profile_id)

        if media_type:
            stmt = stmt.where(ProfileMediaModel.media_type == media_type)

        stmt = stmt.order_by(ProfileMediaModel.order)

        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_profile_photos(session: AsyncSession, profile_id: int) -> List[ProfileMediaModel]:
        """Возвращает все фотографии профиля, отсортированные по порядку"""
        return await ProfileMedia.get_profile_media(session, profile_id, "photo")

    @staticmethod
    async def get_profile_videos(session: AsyncSession, profile_id: int) -> List[ProfileMediaModel]:
        """Возвращает все видео профиля, отсортированные по порядку"""
        return await ProfileMedia.get_profile_media(session, profile_id, "video")

    @staticmethod
    async def get_first_photo(
        session: AsyncSession, profile_id: int
    ) -> Optional[ProfileMediaModel]:
        """Возвращает первое фото профиля (с минимальным order)"""
        stmt = (
            select(ProfileMediaModel)
            .where(ProfileMediaModel.profile_id == profile_id)
            .where(ProfileMediaModel.media_type == "photo")
            .order_by(ProfileMediaModel.order)
            .limit(1)
        )

        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def delete_by_id(session: AsyncSession, id: int):
        """Удаляет медиа по ID"""
        stmt = delete(ProfileMediaModel).where(ProfileMediaModel.id == id)
        await session.execute(stmt)
        await session.commit()
        logger.log("DATABASE", f"Удалил медиа с ID: {id}")

    @staticmethod
    async def delete_profile_media(session: AsyncSession, profile_id: int):
        """Удаляет все медиа профиля"""
        stmt = delete(ProfileMediaModel).where(ProfileMediaModel.profile_id == profile_id)
        result = await session.execute(stmt)
        await session.commit()
        logger.log("DATABASE", f"Удалил {result.rowcount} медиа для профиля {profile_id}")

    @staticmethod
    async def delete_profile_photos(session: AsyncSession, profile_id: int):
        """Удаляет все фотографии профиля"""
        stmt = (
            delete(ProfileMediaModel)
            .where(ProfileMediaModel.profile_id == profile_id)
            .where(ProfileMediaModel.media_type == "photo")
        )
        result = await session.execute(stmt)
        await session.commit()
        logger.log("DATABASE", f"Удалил {result.rowcount} фото для профиля {profile_id}")

    @staticmethod
    async def delete_profile_videos(session: AsyncSession, profile_id: int):
        """Удаляет все видео профиля"""
        stmt = (
            delete(ProfileMediaModel)
            .where(ProfileMediaModel.profile_id == profile_id)
            .where(ProfileMediaModel.media_type == "video")
        )
        result = await session.execute(stmt)
        await session.commit()
        logger.log("DATABASE", f"Удалил {result.rowcount} видео для профиля {profile_id}")

    @classmethod
    async def add_media(
        cls, session: AsyncSession, profile_id: int, media_url: str, media_type: str, order: int = 1
    ) -> ProfileMediaModel:
        """Добавляет новое медиа к профилю"""

        media_data = {
            "profile_id": profile_id,
            "media_type": media_type,
            "media": media_url,
            "order": order,
        }

        obj = await cls.create(session, **media_data)
        logger.log("DATABASE", f"Добавил {media_type} для профиля {profile_id}")
        return obj

    @classmethod
    async def add_multiple_photos(
        cls, session: AsyncSession, profile_id: int, photo_urls: list[str]
    ) -> list[ProfileMediaModel]:
        """Добавляет несколько фотографий к профилю"""
        photos = []
        for i, photo_url in enumerate(photo_urls, 1):
            photo = await cls.add_media(
                session=session,
                profile_id=profile_id,
                media_url=photo_url,
                media_type="photo",
                order=i,
            )
            photos.append(photo)
        return photos

    @classmethod
    async def update_media_order(cls, session: AsyncSession, media_id: int, new_order: int):
        """Обновляет порядок медиа"""
        media = await cls.get_by_id(session, media_id)
        if media:
            media.order = new_order
            await session.commit()
            logger.log("DATABASE", f"Обновил порядок медиа {media_id} на {new_order}")
            return media
        return None
