from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data.config import TG_TOKEN
from app.middlewares.i18n import i18n

storage = MemoryStorage()
bot = Bot(TG_TOKEN, parse_mode="html")
dp = Dispatcher(bot=bot, storage=storage)

_ = i18n.gettext