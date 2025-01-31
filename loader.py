from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n

from data import config
from utils.logging import logger

if config.REDIS_URL:
    from aiogram.fsm.storage.redis import RedisStorage
    from redis.asyncio.client import Redis

    storage = RedisStorage(Redis.from_url(config.REDIS_URL))
    logger.info("Storage: Redis")
elif not config.REDIS_URL:
    from aiogram.fsm.storage.memory import MemoryStorage

    storage = MemoryStorage()
    logger.info("Storage: Default")

bot = Bot(
    config.TG_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher(bot=bot, storage=storage)

i18n = I18n(path=config.LOCALES_DIR, domain=config.I18N_DOMAIN)
_ = i18n.gettext
