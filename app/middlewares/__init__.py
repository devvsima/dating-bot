from aiogram import Dispatcher

from app.middlewares.i18n import i18n_middleware
from app.routers import admin_router, start_router, user_router
from database.connect import async_session

from .admin import AdminMiddleware
from .database import DatabaseMiddleware
from .start import StartMiddleware
from .user import UsersMiddleware


def setup_middlewares(dp: Dispatcher) -> None:
    dp.update.middleware(DatabaseMiddleware(async_session))

    start_router.message.middleware(StartMiddleware())
    admin_router.message.middleware(AdminMiddleware())
    user_router.message.middleware(UsersMiddleware())
    user_router.callback_query.middleware(UsersMiddleware())

    start_router.message.middleware(i18n_middleware)
    admin_router.message.middleware(i18n_middleware)
    user_router.message.middleware(i18n_middleware)
