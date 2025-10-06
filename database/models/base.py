from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime, func
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
