from typing import List

from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, Integer, String, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from utils.logging import logger

from .base import BaseModel


class Profile(BaseModel):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    find_gender: Mapped[str] = mapped_column(String(20), nullable=False)
    city: Mapped[str] = mapped_column(String(200), nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(900), nullable=True)
    instagram: Mapped[str] = mapped_column(String(200), nullable=True)
    is_shared_location: Mapped[bool] = mapped_column(server_default="False", nullable=False)
    is_active: Mapped[bool] = mapped_column(server_default="True", nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="profile")  # type: ignore
    profile_media: Mapped[List["ProfileMedia"]] = relationship(  # type: ignore
        back_populates="profile", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("gender IN ('male', 'female')", name="gender_check"),
        CheckConstraint("find_gender IN ('male', 'female', 'all')", name="find_gender_check"),
    )

    @classmethod
    async def create_or_update(cls, session: AsyncSession, **kwargs):
        """Создает профиль пользователя, если профиль есть - обновляет его"""
        from .profile_media import ProfileMedia

        profile_id = kwargs.pop("id")  # Извлекаем id профиля
        photo_url = kwargs.pop(
            "photo", None
        )  # Извлекаем photo, если есть (для обратной совместимости)
        photos = kwargs.pop("photos", None)  # Извлекаем список фото

        obj = await cls.get_by_id(session, profile_id)
        is_new = False

        if obj:
            # Обновляем существующий профиль
            for key, value in kwargs.items():
                setattr(obj, key, value)
            await session.commit()
        else:
            # Создаем новый профиль
            obj = await cls.create_profile(session, id=profile_id, **kwargs)
            is_new = True
            logger.log("DATABASE", f"{profile_id}: создал анкету")

        # Обрабатываем фото
        if photos:
            # Удаляем все старые фото профиля
            await ProfileMedia.delete_profile_photos(session, profile_id)

            # Добавляем новые фото
            for i, photo_file_id in enumerate(photos, 1):
                await ProfileMedia.add_media(
                    session=session,
                    profile_id=profile_id,
                    media_url=photo_file_id,
                    media_type="photo",
                    order=i,
                )
        elif photo_url:
            # Обратная совместимость - если передано одно фото
            await ProfileMedia.delete_profile_photos(session, profile_id)

            await ProfileMedia.add_media(
                session=session,
                profile_id=profile_id,
                media_url=photo_url,
                media_type="photo",
                order=1,
            )
        else:
            logger.log("DATABASE", "Error to creating profile")
        return obj, is_new
