from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.referal import ReferalModel
from database.queries.base import BaseService


class Referal(BaseService):
    model = ReferalModel

    @staticmethod
    async def get_invites_count(session: AsyncSession, inviter_id: int) -> int:
        """Получает количество людей, которых пригласил пользователь"""
        query = select(func.count(ReferalModel.id)).where(ReferalModel.inviter_id == inviter_id)
        result = await session.execute(query)
        count = result.scalar()
        return count or 0
