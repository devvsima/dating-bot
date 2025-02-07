from sqlalchemy import BigInteger, String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    language: Mapped[str] = mapped_column(String, default="en")
    referral: Mapped[int] = mapped_column(Integer, default=0)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)

    # profile: Mapped["Profile"] = relationship(backref="user_id")

    def __repr__(self):
        return f"{self.id} | {self.username}"
