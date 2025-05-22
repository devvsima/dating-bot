from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.services.base import BaseService
from utils.logging import logger

from ..models.match import MatchModel


class Match(BaseService):
    model = MatchModel

    @staticmethod
    async def create(session: AsyncSession, sender_id: int, receiver_id: int) -> bool:
        """
        Добавляет лайк в БД, если он уже есть - ничего не делает.
        Возвращает True, если запись была создана, иначе False.
        """
        existing_match = await session.execute(
            select(MatchModel).where(
                (MatchModel.sender_id == sender_id) & (MatchModel.receiver_id == receiver_id)
            )
        )
        if existing_match.scalar():  # Если запись уже существует
            logger.log("DATABASE", f"{sender_id} & {receiver_id}: лайк повторился")
            return False

        # Если записи нет, добавляем новую
        stmt = insert(MatchModel).values(sender_id=sender_id, receiver_id=receiver_id)
        await session.execute(stmt)
        await session.commit()

        logger.log("DATABASE", f"{sender_id}: лайкнул пользователя {receiver_id}")
        return True

    @staticmethod
    async def get_user_matchs(session: AsyncSession, id: int) -> list:
        """Возвращает список пользователей, которые лайкнули анкету"""
        result = await session.execute(
            select(MatchModel.sender_id).where(MatchModel.receiver_id == id)
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
        logger.log("DATABASE", f"{sender_id} & {receiver_id}: лайк удален")

    @staticmethod
    async def delete_all_by_sender(session: AsyncSession, sender_id: int) -> None:
        """
        Удаляет все записи, где пользователь лайкнул кого-то (по sender_id).
        """
        await session.execute(
            MatchModel.__table__.delete().where(MatchModel.sender_id == sender_id)
        )
        await session.commit()
        logger.log("DATABASE", f"Все лайки пользователя {sender_id} были удалены")
