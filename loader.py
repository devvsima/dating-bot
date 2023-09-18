from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data.config import token_api
from app.middlewares.i18n import setup_middleware

storage = MemoryStorage()

bot = Bot(token=token_api, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage, run_tasks_by_default=True)

i18n = setup_middleware(dp)
_ = i18n.gettext