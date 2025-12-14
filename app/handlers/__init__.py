from aiogram import Dispatcher
from aiogram.types import ErrorEvent

from utils.logging import logger

from .admin import admin_router
from .common import common_router
from .dating import dating_router, registration_router
from .other import voide_router


def setup_handlers(dp: Dispatcher) -> None:
    async def _error(event: ErrorEvent):
        logger.exception(event.exception)

    dp.errors.register(_error)

    dp.include_routers(
        common_router,
        registration_router,
        dating_router,
        admin_router,
        voide_router,
    )
