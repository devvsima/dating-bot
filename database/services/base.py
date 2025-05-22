from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Mapped


class BaseService:
    model: Mapped = None

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs):
        """Создаёт новую запись в таблице."""
        instance = cls.model(**kwargs)
        session.add(instance)
        await session.commit()
        return instance

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int):
        """Получает запись по ID."""
        result = await session.execute(select(cls.model).where(cls.model.id == id))
        return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls, session: AsyncSession, **filters):
        """Получает все записи с возможностью фильтрации."""
        query = select(cls.model)
        if filters:
            query = query.filter_by(**filters)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def update(cls, session: AsyncSession, id: int, **kwargs):
        """Обновляет запись по ID."""
        instance = await cls.get_by_id(session, id)
        if not instance:
            return None
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await session.commit()
        return instance

    @classmethod
    async def delete(cls, session: AsyncSession, id: int):
        """Удаляет запись по ID."""
        instance = await cls.get_by_id(session, id)
        if instance:
            await session.delete(instance)
            await session.commit()
        return instance

    @classmethod
    async def delete_by_filter(cls, session: AsyncSession, **filters):
        """Удаляет записи по фильтру."""
        query = delete(cls.model)
        if filters:
            query = query.filter_by(**filters)
        await session.execute(query)
        await session.commit()

    @classmethod
    async def paginate(cls, session: AsyncSession, page: int, page_size: int, **filters):
        """Возвращает записи с пагинацией."""
        query = select(cls.model)
        if filters:
            query = query.filter_by(**filters)
        result = await session.execute(query.offset((page - 1) * page_size).limit(page_size))
        return result.scalars().all()

    @classmethod
    async def get_or_create(cls, session: AsyncSession, defaults: dict = None, **filters):
        """
        Получает запись по фильтрам или создаёт новую, если запись не найдена.
        :param session: AsyncSession
        :param defaults: Словарь значений по умолчанию для создания новой записи
        :param filters: Фильтры для поиска записи
        :return: (instance, created) - объект и флаг, создан ли он
        """
        instance = await cls.get_all(session, **filters)
        if instance:
            return instance[0], False  # Возвращаем первую найденную запись
        data = {**filters, **(defaults or {})}
        instance = await cls.create(session, **data)
        return instance, True
