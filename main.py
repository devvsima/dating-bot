from aiogram import Bot, Dispatcher, executor, types

# from aiogram.utils.callback_data import CallbackData
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.middlewares import BaseMiddleware

# from aiogram.dispatcher.filters import Text
from colorama import init, Style, Fore

from loader import dp, bot

# импорт скриптов
from database import *
from app import *
from config import *
from utils import *


async def start_up(_):
    await db_start()
    print(Fore.GREEN + "  [ Bot_start_up ] ")


class Test(BaseMiddleware):
    async def on_pre_process_update(self, update: types.update, data: dict):
        print("Target")


# старт скрипта
if __name__ == "__main__":
    dp.middleware.setup(Test())
    executor.start_polling(
        dp,
        on_startup=start_up,
        skip_updates=True,
    )
