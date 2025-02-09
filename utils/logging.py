from logging import getLogger

from loguru import logger

from data.config import DIR

logger.add(
    f"{DIR}/logs/logs.log",
    format="[{time}] [{level}] [{file.name}:{line}]  {message}",
    level="DEBUG",
    rotation="1 month",
    compression="zip",
)

getLogger("aiogram").addFilter(
    lambda r: r.getMessage().find("Field 'database_user' doesn't exist in") == -1
)
