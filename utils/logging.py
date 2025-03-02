from logging import getLogger

from loguru import logger

from data.config import DIR, TIME_ZONE

# logger.level("MESSAGE", no=15, color="<blue>")
LOG_DIR = f"{DIR}/logs"
FORMAT = "[{time}] [{level}] [{file.name}:{line}]  {message}"
ROTATION = "1 month"
COMPRESSION = "zip"

logger.add(
    f"{LOG_DIR}/logs.log",
    format=FORMAT,
    level="DEBUG",
    rotation=ROTATION,
    compression=COMPRESSION,
)

logger.level("BOT", no=18, color="<green>", icon="🚨")
logger.level("MESSAGE", no=15, color="<blue>", icon="✍️")
logger.level("CALLBACK", no=15, color="<blue>", icon="📩")
logger.level("DATABASE", no=17, color="<magenta>", icon="💾")

getLogger("aiogram").addFilter(
    lambda r: r.getMessage().find("Field 'database_user' doesn't exist in") == -1
)
