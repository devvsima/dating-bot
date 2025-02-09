from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from utils.logging import logger

from ..models.match import MatchModel


class Match:
    @staticmethod
    async def add(session: AsyncSession, sender_id: int, receiver_id: int) -> None:
        """Добавляет лайк в БД, если он уже есть - ничего не делает"""
        result = await session.execute(
            select(MatchModel).where(
                MatchModel.sender_id == sender_id, MatchModel.receiver_id == receiver_id
            )
        )
        existing_like = result.scalar()

        if existing_like:
            logger.info(f"Повторился лайк: {sender_id} & {receiver_id}")
        else:
            stmt = insert(MatchModel).values(sender_id=sender_id, receiver_id=receiver_id)
            await session.execute(stmt)
            await session.commit()
            logger.info(f"User: {sender_id} | лайкнул пользователя {receiver_id}")

    @staticmethod
    async def get_all(session: AsyncSession, user_id: int) -> list:
        """Возвращает список пользователей, которые лайкнули анкету"""
        result = await session.execute(
            select(MatchModel.sender_id).where(MatchModel.receiver_id == user_id)
        )

        return [row[0] for row in result.fetchall()]

    @staticmethod
    async def delete(session: AsyncSession, receiver_id: int, sender_id: int) -> None:
        """Удаляет лайк из БД"""
        await session.execute(
            MatchModel.__table__.delete().where(
                (MatchModel.sender_id == sender_id) & (MatchModel.receiver_id == receiver_id)
            )
        )
        await session.commit()
        logger.info(f"{sender_id} & {receiver_id} | лайк удален")
