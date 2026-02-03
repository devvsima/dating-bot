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


def apply_common_middlewares(router, middleware_class, include_throttling=True):
    """Применяет стандартный набор middleware к роутеру."""
    router.message.middleware(LoggingMiddleware())
    router.callback_query.middleware(LoggingMiddleware())

    if include_throttling:
        router.message.middleware(ThrottlingMiddleware())
        router.callback_query.middleware(ThrottlingMiddleware())

    router.message.middleware(middleware_class())
    router.callback_query.middleware(middleware_class())
    router.message.middleware(i18n_middleware)
    router.callback_query.middleware(i18n_middleware)


def setup_middlewares(dp: Dispatcher) -> None:
    dp.update.middleware(DatabaseMiddleware(async_session))

    apply_common_middlewares(common_router, CommonMiddleware)
    apply_common_middlewares(registration_router, Registration_Middleware)
    apply_common_middlewares(dating_router, DatingMiddleware)
    apply_common_middlewares(admin_router, AdminMiddleware, include_throttling=False)
    apply_common_middlewares(voide_router, VoideMiddleware)
