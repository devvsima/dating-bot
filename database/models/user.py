from sqlalchemy import BigInteger, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

ROLES = {
    0: "banned",
    1: "user",
    2: "sponsor",
    3: "moderator",
    4: "admin",
    5: "owner",
}


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    language: Mapped[str] = mapped_column(String, default="en")
    referral: Mapped[int] = mapped_column(Integer, default=0)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)

    profile: Mapped["ProfileModel"] = relationship(
        "ProfileModel", uselist=False, back_populates="user"
    )
