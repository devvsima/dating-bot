from aiogram import Dispatcher, executor
from app import middlewares ,filters, handlers
from loader import dp, bot
from utils.logging import logger


async def on_startup(_):
    from app.commands import set_default_commands
    await set_default_commands()
    logger.info("~ Bot_startup")

async def on_shutdown(dispatcher: Dispatcher):
    logger.info("~ Shutting down...")


if __name__ == "__main__":
    from app.middlewares import setup_middlewares
    setup_middlewares(dp)
    executor.start_polling(     
        dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
    )
