from typing import Any, Optional, Tuple
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram import types
from data.config import I18N_DOMAIN, DIR

async def get_lang(user_id):
    return None

class ACLMidlleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        user = types.User.get_current()
        return await get_lang(user.id) or user.locale

def setup_middleware(dp):
    i18n = ACLMidlleware(I18N_DOMAIN, DIR)
    dp.middleware.setup(i18n)
    return i18n