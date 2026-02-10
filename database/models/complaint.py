from sqlalchemy import BigInteger, ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel, StatusMixin


class ComplaintStatus(StatusMixin):
    Rejected = 0
    Pending = 1
    Accepted = 2


class ProfileComplaint(BaseModel):
    __tablename__ = "profile_complaints"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    reason: Mapped[str] = mapped_column(String(250), nullable=True)
    status: Mapped[int] = mapped_column(Integer, server_default="1", nullable=False)

    @classmethod
    async def create_complaint(cls, session: AsyncSession, **kwargs):
        """Создает новую жалобу"""
        instance = cls(**kwargs)
        session.add(instance)
        await session.commit()
        return instance

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int):
        """Получает жалобу по ID"""
        result = await session.execute(select(cls).where(cls.id == id))
        return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls, session: AsyncSession, **filters):
        """Получает все жалобы с возможностью фильтрации"""
        query = select(cls)
        if filters:
            query = query.filter_by(**filters)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def update_complaint(cls, session: AsyncSession, id: int, **kwargs):
        """Обновляет жалобу по ID"""
        instance = await cls.get_by_id(session, id)
        if not instance:
            return None
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await session.commit()
        return instance
