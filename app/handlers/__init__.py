
from aiogram import Dispatcher
from aiogram.types import ErrorEvent

from utils import logger

from .admin import router as admin_router
from .user import router as user_router
from .user.start import start_router


def setup_handlers(dp: Dispatcher) -> None:
    @dp.error()
    async def _error(event: ErrorEvent):
        logger.exception(event.exception)

    dp.include_routers(start_router, user_router, admin_router)
