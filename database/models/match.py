from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Match(BaseModel):
    __tablename__ = "matchs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    message: Mapped[str] = mapped_column(nullable=True)
