from aiogram import Dispatcher
from .user import UsersMiddleware
from .start import StartMiddleware
from .admin import AdminMiddleware
from app.routers import start_router, admin_router
from app.middlewares.i18n import i18n_middleware


def setup_middlewares(dp: Dispatcher) -> None:
    start_router.message.middleware(StartMiddleware())
    admin_router.message.middleware(AdminMiddleware())
    
    dp.update.middleware(UsersMiddleware())
    dp.message.middleware(i18n_middleware)
