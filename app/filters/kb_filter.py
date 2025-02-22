from aiogram.filters.callback_data import CallbackData


class LangCallback(CallbackData, prefix="lang"):
    lang: str
