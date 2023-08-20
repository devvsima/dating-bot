from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import *

storage = MemoryStorage()
bot = Bot(token_api)
dp = Dispatcher(bot=bot, storage=storage)
