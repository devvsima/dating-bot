import asyncio

from app.middlewares import setup_middlewares
from loader import dp, bot
from utils.logging import logger

async def on_startup() -> None:
    from app.others.commands import set_default_commands
    await set_default_commands()
    logger.info("~ Bot startup")

async def on_shutdown() -> None:
    logger.info("~ Bot shutting down...")

    
async def main():
    setup_middlewares(dp)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    from app.handlers import setup_handlers
    setup_handlers(dp)
    from data.config import SKIP_UPDATES
    await dp.start_polling(     
        bot,
        skip_updates=SKIP_UPDATES,
    )


if __name__ == "__main__":
    asyncio.run(main())
