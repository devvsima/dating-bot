from aiogram import executor, types
from aiogram.dispatcher.middlewares import BaseMiddleware

from colorama import Fore

from app import middlewares, filters, handlers



async def start_up(_):

    print(Fore.GREEN + "  [ Bot_start_up ]  " + Fore.WHITE)


class Target(BaseMiddleware):
    async def on_pre_process_update(self, update: types.update, data: dict):
        print("Target")


if __name__ == "__main__":
    from loader import dp, bot
    dp.middleware.setup(Target())
    executor.start_polling(
        dp,
        on_startup=start_up,
        skip_updates=True,
    )
