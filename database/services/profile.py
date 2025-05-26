from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from database.services.base import BaseService
from utils.logging import logger

from ..models.profile import ProfileModel, ProfilePhotoModel


class Profile(BaseService):
    model = ProfileModel

    @staticmethod
    async def get(session: AsyncSession, id: int):
        """Возвращает профиль пользователя с фотографиями"""
        result = await session.execute(
            select(ProfileModel)
            .options(joinedload(ProfileModel.photos))
            .where(ProfileModel.id == id)
        )
        return result.unique().scalar_one_or_none()

    @staticmethod
    async def delete(session: AsyncSession, id: int):
        """Удаляет профиль пользователя"""
        stmt = delete(ProfileModel).where(ProfileModel.id == id)
        await session.execute(stmt)
        await session.commit()
        logger.log("DATABASE", f"{id}: удалил профиль")

    @classmethod
    async def create_or_update(cls, session: AsyncSession, **kwargs):
        """Создает или обновляет профиль пользователя с фотографиями"""
        photos = kwargs.pop("photos", None)  # список строк (пути/имена файлов)
        obj = await cls.get_by_id(session, kwargs["id"])
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            if photos is not None:
                # Удаляем старые фото
                obj.photos.clear()
                # Добавляем новые фото (до 3)
                for photo in photos[:3]:
                    obj.photos.append(ProfilePhotoModel(photo=photo))
            await session.commit()
            return obj, False
        obj = await cls.create(session, **kwargs)
        if photos is not None:
            for photo in photos[:3]:
                obj.photos.append(ProfilePhotoModel(photo=photo))
            await session.commit()
        logger.log("DATABASE", f"{kwargs['id']}: создал анкету")
        return obj, True
