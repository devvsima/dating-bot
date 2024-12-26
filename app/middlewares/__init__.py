from aiogram import Dispatcher

from .user import UsersMiddleware
from app.middlewares.i18n import i18n


def setup_middlewares(dp: Dispatcher) -> None:
    dp.middleware.setup(UsersMiddleware())
    dp.middleware.setup(i18n)
