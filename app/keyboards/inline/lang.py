from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import i18n

language_dict = {
    "ru": "Русский",
    "uk": "Українська",
    "en": "English",
}


class LangCallback(CallbackData, prefix="lang"):
    lang: str


def lang_ikb():
    builder = InlineKeyboardBuilder()

    [
        builder.button(text=language_dict[lang], callback_data=LangCallback(lang=lang))
        for lang in i18n.available_locales
    ]

    return builder.as_markup()
