from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

created_at = Annotated[
    datetime,
    mapped_column(DateTime, server_default=func.now(), nullable=True),
]
updated_at = Annotated[
    datetime,
    mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=True),
]


class BaseModel(DeclarativeBase):
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                col.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.name} {', '.join(cols)}>"
