from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

created_at = Annotated[
    datetime,
    mapped_column(DateTime, server_default=func.now(), nullable=True),
]
updated_at = Annotated[
    datetime,
    mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=True),
]


class BaseModel(DeclarativeBase):
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {', '.join(cols)}>"

    # Базовые методы запросов (из BaseService)
    @classmethod
    async def create(cls, session: AsyncSession, **kwargs):
        """Создаёт новую запись в таблице."""
        instance = cls(**kwargs)
        session.add(instance)
        await session.commit()
        return instance

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int):
        """Получает запись по ID."""
        result = await session.execute(select(cls).where(cls.id == id))
        return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls, session: AsyncSession, **filters):
        """Получает все записи с возможностью фильтрации."""
        query = select(cls)
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
        query = delete(cls)
        if filters:
            query = query.filter_by(**filters)
        await session.execute(query)
        await session.commit()

    @classmethod
    async def paginate(cls, session: AsyncSession, page: int, page_size: int, **filters):
        """Возвращает записи с пагинацией."""
        query = select(cls)
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


class StatusMixin:
    """Миксин для автоматического создания маппинга статусов"""

    def __init_subclass__(cls, **kwargs):
        """Автоматически создает маппинги при наследовании"""
        super().__init_subclass__(**kwargs)
        cls._build_mappings()

    @classmethod
    def _build_mappings(cls):
        """Строит маппинги статусов"""
        status_map = {}
        reverse_map = {}

        for attr_name in dir(cls):
            if not attr_name.startswith("_") and not callable(getattr(cls, attr_name)):
                attr_value = getattr(cls, attr_name)
                if isinstance(attr_value, int):
                    # CamelCase -> readable
                    readable_name = "".join(
                        [" " + c if c.isupper() else c for c in attr_name]
                    ).strip()
                    status_map[attr_value] = readable_name
                    reverse_map[readable_name.lower()] = attr_value

        cls._STATUS_MAP = status_map
        cls._REVERSE_MAP = reverse_map

    @classmethod
    def get_status_name(cls, status: int) -> str:
        """Возвращает название статуса по числу"""
        return cls._STATUS_MAP.get(status, "Unknown")

    @classmethod
    def get_status_value(cls, name: str) -> int | None:
        """Возвращает числовое значение по названию"""
        return cls._REVERSE_MAP.get(name.lower())

    @classmethod
    def all_statuses(cls) -> dict:
        """Возвращает все статусы"""
        return cls._STATUS_MAP.copy()

    @classmethod
    def get_choices(cls) -> list[tuple[int, str]]:
        """Возвращает список для форм (value, label)"""
        return [(k, v) for k, v in cls._STATUS_MAP.items()]
