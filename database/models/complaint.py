from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel, StatusMixin


class ComplaintStatus(StatusMixin):
    Rejected = 0
    Pending = 1
    Accepted = 2


class ProfileComplaintsModel(BaseModel):
    __tablename__ = "profile_complaints"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    reason: Mapped[str] = mapped_column(String(250), nullable=True)
    status: Mapped[int] = mapped_column(Integer, server_default="1", nullable=False)
