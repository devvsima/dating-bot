from aiogram import Dispatcher

from app.middlewares.i18n import i18n_middleware
from app.routers import (
    admin_router,
    common_router,
    dating_router,
    registration_router,
    voide_router,
)
from database.connect import async_session

from .admin import AdminMiddleware
from .common import CommonMiddleware
from .database import DatabaseMiddleware
from .dating import DatingMiddleware, Registration_Middleware
from .logging import LoggingMiddleware
from .throttling import ThrottlingMiddleware
from .voide import VoideMiddleware


def setup_middlewares(dp: Dispatcher) -> None:
    dp.update.middleware(DatabaseMiddleware(async_session))

    common_router.message.middleware(LoggingMiddleware())
    common_router.callback_query.middleware(LoggingMiddleware())
    common_router.message.middleware(ThrottlingMiddleware())
    common_router.callback_query.middleware(ThrottlingMiddleware())
    common_router.message.middleware(CommonMiddleware())
    common_router.callback_query.middleware(CommonMiddleware())
    common_router.message.middleware(i18n_middleware)
    common_router.callback_query.middleware(i18n_middleware)

    registration_router.message.middleware(LoggingMiddleware())
    registration_router.callback_query.middleware(LoggingMiddleware())
    registration_router.message.middleware(ThrottlingMiddleware())
    registration_router.callback_query.middleware(ThrottlingMiddleware())
    registration_router.message.middleware(Registration_Middleware())
    registration_router.callback_query.middleware(Registration_Middleware())
    registration_router.message.middleware(i18n_middleware)
    registration_router.callback_query.middleware(i18n_middleware)

    dating_router.message.middleware(LoggingMiddleware())
    dating_router.callback_query.middleware(LoggingMiddleware())
    dating_router.message.middleware(ThrottlingMiddleware())
    dating_router.callback_query.middleware(ThrottlingMiddleware())
    dating_router.message.middleware(DatingMiddleware())
    dating_router.callback_query.middleware(DatingMiddleware())
    dating_router.message.middleware(i18n_middleware)
    dating_router.callback_query.middleware(i18n_middleware)

    admin_router.message.middleware(LoggingMiddleware())
    admin_router.callback_query.middleware(LoggingMiddleware())
    admin_router.message.middleware(AdminMiddleware())
    admin_router.message.middleware(i18n_middleware)

    voide_router.message.middleware(LoggingMiddleware())
    voide_router.message.middleware(ThrottlingMiddleware())
    voide_router.callback_query.middleware(ThrottlingMiddleware())
    voide_router.message.middleware(VoideMiddleware())

    voide_router.message.middleware(i18n_middleware)
