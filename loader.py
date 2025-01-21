from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from app.middlewares.i18n import i18n

from utils.logging import logger

# if config.REDIS_HOST and config.REDIS_PORT:
#     from aiogram.contrib.fsm_storage.redis import RedisStorage2
#     storage = RedisStorage2(config.REDIS_HOST, config.REDIS_PORT, db=config.REDIS_DB)
#     logger.info("Storage: Redis")
# else:
from aiogram.contrib.fsm_storage.memory import MemoryStorage
storage = MemoryStorage()
logger.info("Storage: Default")
    
    
bot = Bot(config.TG_TOKEN, parse_mode="html")
dp = Dispatcher(bot=bot, storage=storage)

_ = i18n.gettext