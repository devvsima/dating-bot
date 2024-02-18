from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data.config import token_api
from app.middlewares.i18n import setup_middleware

storage = MemoryStorage()
bot = Bot(token_api, parse_mode="html")
dp = Dispatcher(bot=bot, storage=storage)

i18n = setup_middleware(dp)
_ = i18n.gettext