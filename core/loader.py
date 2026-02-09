from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n

from core.config import LOCALES_DIR, redis, tgbot
from utils.logging import logger

# -< FSM Storage>-
if redis.URL:
    from aiogram.fsm.storage.redis import RedisStorage
    from redis.asyncio.client import Redis

    storage = RedisStorage(Redis.from_url(redis.URL))
    logger.log("BOT", "Storage: Redis")
elif not redis.URL:
    from aiogram.fsm.storage.memory import MemoryStorage

    storage = MemoryStorage()
    logger.log("BOT", "Storage: Default")

# -< Bot >-
bot_properties = DefaultBotProperties(
    parse_mode=ParseMode.HTML,
)
bot = Bot(
    token=tgbot.BOT_TOKEN,
    default=bot_properties,
)

dp = Dispatcher(bot=bot, storage=storage)

i18n = I18n(path=LOCALES_DIR, domain=tgbot.I18N_DOMAIN, default_locale="en")
_ = i18n.gettext
__ = i18n.lazy_gettext
