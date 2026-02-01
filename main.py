import asyncio

from aiohttp import web

from app.commands import set_default_commands
from app.handlers import setup_handlers
from app.middlewares import setup_middlewares
from data.config import tgbot
from loader import bot, dp
from utils.logging import logger
from webhook import run_polling, run_webhook


async def on_startup() -> None:
    """Действия при запуске бота."""
    if tgbot.SET_COMMANDS:
        await set_default_commands()
    logger.log("BOT", "~ Bot startup")


async def on_shutdown() -> None:
    """Действия при остановке бота."""
    logger.log("BOT", "~ Bot shutting down...")
    await bot.session.close()


async def main():
    """Главная функция запуска бота."""
    setup_middlewares(dp)
    setup_handlers(dp)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    if tgbot.IS_WEBHOOK:
        app = web.Application()
        await run_webhook(app, bot, dp)
    else:
        await run_polling(bot, dp)


if __name__ == "__main__":
    asyncio.run(main())
