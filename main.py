from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.middlewares import BaseMiddleware

from colorama import init, Style, Fore

# скрипты
from loader import dp, bot
from database import *
from app import *
from utils import *


async def start_up(_):
    await db_start()
    print(Fore.GREEN + "  [ Bot_start_up ]  " + Fore.WHITE)


class Test(BaseMiddleware):
    async def on_pre_process_update(self, update: types.update, data: dict):
        print("Target")


if __name__ == "__main__":
    dp.middleware.setup(Test())
    executor.start_polling(
        dp,
        on_startup=start_up,
        skip_updates=True,
    )
