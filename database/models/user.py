from sqlalchemy import BigInteger, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship

from utils.logging import logger

from .base import BaseModel, StatusMixin


class UserStatus(StatusMixin):
    Banned = 0
    User = 1
    Sponsor = 2
    Moderator = 3
    Admin = 4
    Owner = 5


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(70), nullable=True)
    language: Mapped[str] = mapped_column(String(10), server_default="en")
    status: Mapped[int] = mapped_column(Integer, server_default="1")

    profile: Mapped["Profile"] = relationship(  # type: ignore
        "Profile", uselist=False, back_populates="user"
    )

    @staticmethod
    async def get_with_profile(session: AsyncSession, id: int):
        """Возвращает пользователя и его профиль"""
        result = await session.execute(
            select(User).options(joinedload(User.profile)).where(User.id == id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_or_create(
        session: AsyncSession, id: int, username: str = None, language: str = None
    ) -> tuple["User", bool]:
        """Получает или создает пользователя. Возвращает (user, is_created)"""
        if user := await User.get_with_profile(session, id):
            return user, False
        await User.create_user(session, id=id, username=username, language=language)
        user = await User.get_with_profile(session, id)
        return user, True

    @staticmethod
    async def create_user(
        session: AsyncSession, id: int, username: str = None, language: str = None
    ) -> None:
        """Создает нового пользователя"""
        logger.log("DATABASE", f"New user: {id} (@{username}) {language}")
        session.add(User(id=id, username=username, language=language))
        await session.commit()

    @staticmethod
    async def increment_referral_count(session: AsyncSession, user: "User", num: int = 1) -> None:
        """Добавляет приведенного реферала к пользователю"""
        user.referral += num
        await session.commit()
        logger.log("DATABASE", f"{user.id} (@{user.username}): привел нового пользователя")

    @staticmethod
    async def ban(session: AsyncSession, id: int) -> None:
        """
        Блокирует пользователя:
        - Меняет статус анкеты на неактивный.
        - Меняет статус пользователя на заблокированный.
        - Удаляет все лайки, которые пользователь поставил.
        """
        from .match import Match
        from .profile import Profile

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

        await User.update_user(
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
        from .profile import Profile

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

        await User.update_user(
            session=session,
            id=id,
            status=UserStatus.User,
        )

        logger.log("DATABASE", f"Пользователь {id} был разблокирован.")

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int):
        """Получает пользователя по ID"""
        result = await session.execute(select(cls).where(cls.id == id))
        return result.scalar_one_or_none()

    @classmethod
    async def update_user(cls, session: AsyncSession, id: int, **kwargs):
        """Обновляет пользователя по ID"""
        instance = await cls.get_by_id(session, id)
        if not instance:
            return None
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await session.commit()
        return instance
