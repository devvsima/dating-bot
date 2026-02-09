import asyncio

from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from core.config import tgbot
from utils.logging import logger


async def setup_webhook(app: web.Application, bot: Bot, dp: Dispatcher) -> None:
    """Настраивает вебхук для бота."""
    webhook_url = f"{tgbot.WEBHOOK_URL}{tgbot.WEBHOOK_PATH}"
    await bot.set_webhook(url=webhook_url, secret_token=tgbot.WEBHOOK_SECRET)
    logger.log("BOT", f"Webhook set to: {webhook_url}")

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=tgbot.WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=tgbot.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)


async def run_webhook(app: web.Application, bot: Bot, dp: Dispatcher) -> None:
    """Запускает вебхук сервер."""
    await bot(DeleteWebhook(drop_pending_updates=tgbot.SKIP_UPDATES))
    await setup_webhook(app, bot, dp)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=tgbot.WEBHOOK_HOST, port=tgbot.WEBHOOK_PORT)
    await site.start()

    logger.log("BOT", f"Webhook server started on {tgbot.WEBHOOK_HOST}:{tgbot.WEBHOOK_PORT}")

    try:
        await asyncio.Event().wait()
    finally:
        await runner.cleanup()


async def run_polling(bot: Bot, dp: Dispatcher) -> None:
    """Запускает бота в режиме polling."""
    await bot(DeleteWebhook(drop_pending_updates=tgbot.SKIP_UPDATES))
    logger.log("BOT", "Start polling mode")
    await dp.start_polling(bot)
