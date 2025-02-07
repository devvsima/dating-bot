from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.match import Match
from utils.logging import logger


async def set_new_like(session: AsyncSession, sender_id: int, receiver_id: int) -> None:
    """Добавляет лайк в БД, если он уже есть - ничего не делает"""
    stmt = select(Match).where(Match.sender_id == sender_id, Match.receiver_id == receiver_id)
    result = await session.execute(stmt)
    existing_like = result.scalar()

    if existing_like:
        logger.info(f"Повторился лайк: {sender_id} & {receiver_id}")
    else:
        stmt = insert(Match).values(sender_id=sender_id, receiver_id=receiver_id)
        await session.execute(stmt)
        await session.commit()
        logger.info(f"User: {sender_id} | лайкнул пользователя {receiver_id}")


async def get_profile_likes(session: AsyncSession, user_id: int) -> list:
    """Возвращает список пользователей, которые лайкнули анкету"""
    stmt = select(Match.sender_id).where(Match.receiver_id == user_id)
    result = await session.execute(stmt)

    return [row[0] for row in result.fetchall()]


async def del_like(session: AsyncSession, receiver_id: int, sender_id: int) -> None:
    """Удаляет лайк из БД"""
    stmt = Match.__table__.delete().where(
        (Match.sender_id == sender_id) & (Match.receiver_id == receiver_id)
    )
    await session.execute(stmt)
    await session.commit()
    logger.info(f"{sender_id} & {receiver_id} | лайк удален")
