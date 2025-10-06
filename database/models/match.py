from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel, StatusMixin


# not currently in use
class MatchStatus(StatusMixin):
    Rejected = 0
    Pending = 1
    Accepted = 2


class MatchModel(BaseModel):
    __tablename__ = "matchs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    message: Mapped[str] = mapped_column(String(250), nullable=True)
    status: Mapped[int] = mapped_column(Integer, server_default="1")
