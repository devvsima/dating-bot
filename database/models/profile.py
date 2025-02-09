from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class ProfileModel(BaseModel):
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

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="profile")
