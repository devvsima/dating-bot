from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import database
from utils.logging import logger

if database.URL.startswith("sqlite"):
    logger.log("BOT", "Database: Sqlite")
else:
    logger.log("BOT", "Database: PostgreSql")

async_engine = create_async_engine(
    url=database.URL,
    echo=database.ECHO,
    pool_size=database.POOL_SIZE,
    max_overflow=database.MAX_OVERFLOW,
)
async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Контекстный менеджер для получения сессии базы данных

    ВАЖНО: Commit должен вызываться явно в сервисах!
    Сессия автоматически откатывается при ошибках.

    Использование:
        async with get_session() as session:
            # работа с БД
            users = await User.get_all(session)
            await session.commit()  # Явный commit
    """
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
