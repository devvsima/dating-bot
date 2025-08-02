from typing import List

from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class MediaTypes:
    Photo = "photo"
    Video = "video"


class ProfileMediaModel(BaseModel):
    __tablename__ = "profile_media"

    id: Mapped[int] = mapped_column(BigInteger, autoincrement=True, primary_key=True)
    profile_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False
    )
    media_type: Mapped[str] = mapped_column(String(20), nullable=False)
    order: Mapped[int] = mapped_column(Integer, server_default="1", nullable=False)
    media: Mapped[str] = mapped_column(String(300), nullable=False)

    profile: Mapped["ProfileModel"] = relationship(back_populates="profile_media")

    __table_args__ = (CheckConstraint("media_type IN ('photo', 'video')", name="media_type_check"),)
