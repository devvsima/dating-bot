from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from data.config import database
from utils.logging import logger

from .models.base import BaseModel


if database.DB_URL.startswith("sqlite"):
    logger.info("Database: Sqlite")
else:
    logger.info("Database: PostgreSql")

async_engine = create_async_engine(
    url=database.DB_URL,
    echo=database.ECHO,
    pool_size=database.POOL_SIZE,
    max_overflow=database.MAX_OVERFLOW,
)
async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def create_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


async def drop_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
