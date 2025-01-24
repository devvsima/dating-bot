from aiogram import Dispatcher
from .user import UsersMiddleware
from .start import StartMiddleware
from app.routers import start_router
from app.middlewares.i18n import i18n_middleware

def setup_middlewares(dp: Dispatcher) -> None:
    dp.update.middleware(UsersMiddleware())
    start_router.message.middleware(StartMiddleware())
    dp.update.middleware(i18n_middleware)
    
    