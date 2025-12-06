from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.services.base import BaseService
from utils.logging import logger

from ..models.user import UserModel, UserStatus
from .match import Match
from .profile import Profile


class User(BaseService):
    model = UserModel

    @staticmethod
    async def get_with_profile(session: AsyncSession, id: int):
        """Возвращает пользователя и его профиль"""
        result = await session.execute(
            select(UserModel).options(joinedload(UserModel.profile)).where(UserModel.id == id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_or_create(
        session: AsyncSession, id: int, username: str = None, language: str = None
    ) -> UserModel:
        if user := await User.get_with_profile(session, id):
            return user, False
        await User.create(session, id=id, username=username, language=language)
        user = await User.get_with_profile(session, id)
        return user, True

    @staticmethod
    async def create(
        session: AsyncSession, id: int, username: str = None, language: str = None
    ) -> UserModel:
        """Создает нового пользователя"""
        logger.log("DATABASE", f"New user: {id} (@{username}) {language}")
        session.add(UserModel(id=id, username=username, language=language))
        await session.commit()

    @staticmethod
    async def increment_referral_count(
        session: AsyncSession, user: UserModel, num: int = 1
    ) -> None:
        """Добавляет приведенного реферала к пользователю {inviter_id}"""
        user.referral += num
        await session.commit()
        logger.log("DATABASE", f"{user.id} (@{user.username}): привел нового пользователя")

    async def ban(session: AsyncSession, id: int) -> None:
        """
        Блокирует пользователя:
        - Меняет статус анкеты на неактивный.
        - Меняет статус пользователя на заблокированный.
        - Удаляет все лайки, которые пользователь поставил.
        """
        # Получаем пользователя и его анкету
        user = await User.get_with_profile(session, id)
        if not user:
            logger.log("DATABASE", f"Пользователь с ID {id} не найден.")
            return

        if user.profile:
            await Profile.update(
                session,
                id=id,
                is_active=False,
            )

        await User.update(
            session=session,
            id=id,
            status=UserStatus.Banned,
        )

        # Удаляем все лайки, которые пользователь поставил
        await Match.delete_all_by_sender(session, sender_id=id)

        logger.log("DATABASE", f"Пользователь {id} был заблокирован.")

    @staticmethod
    async def unban(session: AsyncSession, id: int) -> None:
        """
        Разблокирует пользователя:
        - Меняет статус анкеты на активный.
        - Меняет статус пользователя на разблокированный.
        """
        # Получаем пользователя и его анкету
        user = await User.get_with_profile(session, id)
        if not user:
            logger.log("DATABASE", f"Пользователь с ID {id} не найден.")
            return

        if user.profile:
            await Profile.update(
                session,
                id=id,
                is_active=True,
            )

        await User.update(
            session=session,
            id=id,
            status=UserStatus.User,
        )

        logger.log("DATABASE", f"Пользователь {id} был разблокирован.")
