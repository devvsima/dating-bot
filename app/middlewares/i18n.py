from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram import types

from typing import Any, Optional, Tuple

from data.config import I18N_DOMAIN, LOCALES_DIR
from typing import Tuple, Any
async def get_language(id):
    pass

class ACLMidllewaare(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str | None:
        user = types.User.get_current()
        return await get_language(user.id) or user.locale
    
def setup_middleware(dp):
    i18n = ACLMidllewaare(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n 