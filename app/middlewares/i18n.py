from aiogram.types import Update
from aiogram.utils.i18n import I18nMiddleware

from core.loader import i18n


class MyI18nMiddleware(I18nMiddleware):
    async def get_locale(self, event: Update, data: dict) -> str:
        user = data.get("user")
        if user and user.language:
            if user.language in i18n.available_locales:
                return user.language
            return "en"
        return await super().get_locale(event, data)


i18n_middleware = MyI18nMiddleware(i18n)
