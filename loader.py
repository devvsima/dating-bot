from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n

from data.config import BOT_TOKEN, I18N_DOMAIN, LOCALES_DIR, redis
from utils.logging import logger

if redis.URL:
    from aiogram.fsm.storage.redis import RedisStorage
    from redis.asyncio.client import Redis

    storage = RedisStorage(Redis.from_url(redis.URL))
    logger.log("BOT", "Storage: Redis")
elif not redis.URL:
    from aiogram.fsm.storage.memory import MemoryStorage

    storage = MemoryStorage()
    logger.log("BOT", "Storage: Default")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher(bot=bot, storage=storage)

i18n = I18n(path=LOCALES_DIR, domain=I18N_DOMAIN)
_ = i18n.gettext
