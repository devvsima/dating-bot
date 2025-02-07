from sqlalchemy import func, DateTime
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column

from typing import Annotated
from datetime import datetime

created_at = Annotated[datetime, mapped_column(DateTime, default=func.now())]
updated_at = Annotated[datetime, mapped_column(DateTime, default=func.now(), onupdate=func.now())]


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
