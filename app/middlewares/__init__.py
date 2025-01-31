from aiogram import Dispatcher
from .user import UsersMiddleware
from .start import StartMiddleware
from .admin import AdminMiddleware
from app.routers import start_router, admin_router, user_router
from app.middlewares.i18n import i18n_middleware


def setup_middlewares(dp: Dispatcher) -> None:
    start_router.message.middleware(StartMiddleware())

    admin_router.message.middleware(AdminMiddleware())

    user_router.message.middleware(UsersMiddleware())
    user_router.callback_query.middleware(UsersMiddleware())

    start_router.message.middleware(i18n_middleware)
    admin_router.message.middleware(i18n_middleware)
    user_router.message.middleware(i18n_middleware)
