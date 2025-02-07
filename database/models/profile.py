from sqlalchemy import BigInteger, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel

from enum import Enum


# class Gender(Enum):
#     male = "male"
#     female = "female"


# class FindGender(Enum):
#     male = "male"
#     female = "female"
#     all = "all"


class Profile(BaseModel):
    __tablename__ = "profiles"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    name: Mapped[str]
    gender: Mapped[str]
    find_gender: Mapped[str]
    city: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]
    photo: Mapped[str]
    age: Mapped[int]
    description: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
