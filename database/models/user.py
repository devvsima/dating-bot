from sqlalchemy import BigInteger, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class UserRole:
    BANNED = 0
    USER = 1
    SPONSOR = 2
    MODERATOR = 3
    ADMIN = 4
    OWNER = 5


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(70), nullable=True)
    language: Mapped[str] = mapped_column(String(10), default="en")
    referral: Mapped[int] = mapped_column(Integer, default=0)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)

    profile: Mapped["ProfileModel"] = relationship(  # type: ignore
        "ProfileModel", uselist=False, back_populates="user"
    )
