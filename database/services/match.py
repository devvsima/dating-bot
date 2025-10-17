from sqlalchemy import case, insert, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.services.base import BaseService
from utils.logging import logger

from ..models.match import MatchModel, MatchStatus


class Match(BaseService):
    model = MatchModel

    @staticmethod
    async def create(
        session: AsyncSession,
        sender_id: int,
        receiver_id: int,
        mail_text: str | None,
        status: int = 1,
        is_active: bool = True,
    ) -> bool:
        """
        Добавляет лайк в БД, если он уже есть - ничего не делает.
        Возвращает True, если запись была создана, иначе False.
        """
        existing_match = await session.execute(
            select(MatchModel).where(
                or_(
                    # Прямое направление: sender -> receiver
                    (MatchModel.sender_id == sender_id) & (MatchModel.receiver_id == receiver_id),
                    # Обратное направление: receiver -> sender
                    (MatchModel.sender_id == receiver_id) & (MatchModel.receiver_id == sender_id),
                )
                & (MatchModel.is_active == True)
            )
        )
        if existing_match.scalar():  # Если запись уже существует
            logger.log("DATABASE", f"{sender_id} & {receiver_id}: лайк повторился")
            return False

        # Если записи нет, добавляем новую
        stmt = insert(MatchModel).values(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message=mail_text,
            status=status,
            is_active=is_active,
        )
        await session.execute(stmt)
        await session.commit()

        logger.log("DATABASE", f"{sender_id}: лайкнул пользователя {receiver_id}")
        return True

    @staticmethod
    async def get_user_matchs(session: AsyncSession, id: int) -> list:
        """
        Возвращает список пользователей, которые связаны с пользователем через лайки.
        Логика:
        1. Показывать активные лайки (is_active = True)
        2. Показывать лайки, полученные от других пользователей (receiver_id = id)
        3. Показывать взаимные лайки (где пользователь отправитель, но получил ответ status = 2)
        """

        # Выбираем соответствующий ID в зависимости от роли пользователя
        result = await session.execute(
            select(
                case(
                    (
                        MatchModel.receiver_id == id,
                        MatchModel.sender_id,
                    ),  # Если пользователь получатель - возвращаем отправителя
                    (
                        MatchModel.sender_id == id,
                        MatchModel.receiver_id,
                    ),  # Если пользователь отправитель - возвращаем получателя
                ).label("user_id")
            )
            .where(MatchModel.is_active == True)
            .where(
                or_(
                    # Лайки, полученные от других пользователей
                    (MatchModel.receiver_id == id) & (MatchModel.sender_id != id),
                    # Взаимные лайки: пользователь отправил лайк и получил ответ (status = 2)
                    (MatchModel.sender_id == id) & (MatchModel.status == MatchStatus.Accepted),
                )
            )
        )

        return [row[0] for row in result.fetchall()]

    @staticmethod
    async def get(session: AsyncSession, user_id: int, other_user_id: int) -> MatchModel | None:
        """
        Возвращает Match между двумя пользователями в любом направлении.
        Ищет как где user_id отправитель, так и где получатель.
        """
        result = await session.execute(
            select(MatchModel)
            .where(
                or_(
                    # user_id получил лайк от other_user_id
                    (MatchModel.receiver_id == user_id) & (MatchModel.sender_id == other_user_id),
                    # user_id отправил лайк other_user_id
                    (MatchModel.sender_id == user_id) & (MatchModel.receiver_id == other_user_id),
                )
            )
            .order_by(MatchModel.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

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

    @staticmethod
    async def deactivate_all_by_sender(session: AsyncSession, sender_id: int) -> None:
        """
        Деактивирует все записи, где пользователь лайкнул кого-то (устанавливает is_active = False).
        """
        from sqlalchemy import update

        await session.execute(
            update(MatchModel).where(MatchModel.sender_id == sender_id).values(is_active=False)
        )
        await session.commit()
        logger.log("DATABASE", f"Все лайки пользователя {sender_id} были деактивированы")
