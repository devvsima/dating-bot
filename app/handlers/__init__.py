from aiogram import Dispatcher
from aiogram.types import ErrorEvent

from utils.logging import logger

from .admin import router as admin_router
from .user import router as user_router
from .user.start import start_router


def setup_handlers(dp: Dispatcher) -> None:
    async def _error(event: ErrorEvent):
        logger.exception(event.exception)

    dp.errors.register(_error)

    dp.include_routers(start_router, user_router, admin_router)
