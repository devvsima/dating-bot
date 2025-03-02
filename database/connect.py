from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from data.config import database
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
