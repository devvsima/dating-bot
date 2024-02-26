from aiogram import Dispatcher
from .user import UsersMiddleware
from .throttling import ThrottlingMiddleware
from .i18n import I18nMiddleware


def setup_middlewares(dp: Dispatcher) -> None:
    dp.middleware.setup(UsersMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
    # dp.middleware.setup(I18nMiddleware)