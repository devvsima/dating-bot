"""
- Собираем все текста с проекта
pybabel extract --input-dirs=. -o locales/bot.pot --project=bot

- Создаем файлы с переводами на разные языки
pybabel init -i locales/bot.pot -d locales -D bot -l en
pybabel init -i locales/bot.pot -d locales -D bot -l ru
pybabel init -i locales/bot.pot -d locales -D bot -l uk
pybabel init -i locales/bot.pot -d locales -D bot -l fr
pybabel init -i locales/bot.pot -d locales -D bot -l pl
pybabel init -i locales/bot.pot -d locales -D bot -l es
pybabel init -i locales/bot.pot -d locales -D bot -l id

- После того как все текста переведены, нужно скомпилировать все переводы
pybabel compile -d locales -D bot --statistics

pybabel update -i locales/bot.pot -d locales -D bot

"""

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
