from sqlalchemy import BigInteger, ForeignKey, Integer, String, case, insert, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from utils.logging import logger

from .base import BaseModel, StatusMixin


# not currently in use
class MatchStatus(StatusMixin):
    Rejected = 0
    Pending = 1
    Accepted = 2


class Match(BaseModel):
    __tablename__ = "matchs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    message: Mapped[str] = mapped_column(String(250), nullable=True)
    status: Mapped[int] = mapped_column(Integer, server_default="1")
    is_active: Mapped[bool] = mapped_column(server_default="True", nullable=False)

    @staticmethod
    async def create_match(
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
            select(Match).where(
                or_(
                    # Прямое направление: sender -> receiver
                    (Match.sender_id == sender_id) & (Match.receiver_id == receiver_id),
                    # Обратное направление: receiver -> sender
                    (Match.sender_id == receiver_id) & (Match.receiver_id == sender_id),
                )
                & (Match.is_active == True)
            )
        )
        if existing_match.scalar():  # Если запись уже существует
            logger.log("DATABASE", f"{sender_id} & {receiver_id}: лайк повторился")
            return False

        # Если записи нет, добавляем новую
        stmt = insert(Match).values(
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
                        Match.receiver_id == id,
                        Match.sender_id,
                    ),  # Если пользователь получатель - возвращаем отправителя
                    (
                        Match.sender_id == id,
                        Match.receiver_id,
                    ),  # Если пользователь отправитель - возвращаем получателя
                ).label("user_id")
            )
            .where(Match.is_active == True)
            .where(
                or_(
                    # Лайки, полученные от других пользователей
                    (Match.receiver_id == id) & (Match.sender_id != id),
                    # Взаимные лайки: пользователь отправил лайк и получил ответ (status = 2)
                    (Match.sender_id == id) & (Match.status == MatchStatus.Accepted),
                )
            )
        )

        return [row[0] for row in result.fetchall()]

    @staticmethod
    async def get(session: AsyncSession, user_id: int, other_user_id: int):
        """
        Возвращает Match между двумя пользователями в любом направлении.
        Ищет как где user_id отправитель, так и где получатель.
        """
        result = await session.execute(
            select(Match)
            .where(
                or_(
                    # user_id получил лайк от other_user_id
                    (Match.receiver_id == user_id) & (Match.sender_id == other_user_id),
                    # user_id отправил лайк other_user_id
                    (Match.sender_id == user_id) & (Match.receiver_id == other_user_id),
                )
            )
            .order_by(Match.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def delete(session: AsyncSession, receiver_id: int, sender_id: int) -> None:
        """Удаляет лайк из БД"""
        await session.execute(
            Match.__table__.delete().where(
                (Match.sender_id == sender_id) & (Match.receiver_id == receiver_id)
            )
        )
        await session.commit()
        logger.log("DATABASE", f"{sender_id} & {receiver_id}: лайк удален")

    @staticmethod
    async def delete_all_by_sender(session: AsyncSession, sender_id: int) -> None:
        """
        Удаляет все записи, где пользователь лайкнул кого-то (по sender_id).
        """
        await session.execute(Match.__table__.delete().where(Match.sender_id == sender_id))
        await session.commit()
        logger.log("DATABASE", f"Все лайки пользователя {sender_id} были удалены")

    @staticmethod
    async def deactivate_all_by_sender(session: AsyncSession, sender_id: int) -> None:
        """
        Деактивирует все записи, где пользователь лайкнул кого-то (устанавливает is_active = False).
        """
        from sqlalchemy import update

        await session.execute(
            update(Match).where(Match.sender_id == sender_id).values(is_active=False)
        )
        await session.commit()
        logger.log("DATABASE", f"Все лайки пользователя {sender_id} были деактивированы")
