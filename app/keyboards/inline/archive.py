from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from core.loader import _


def check_archive_ikb(language: str) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        resize_keyboard=True,
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Посмотреть", locale=language), callback_data="archive")],
        ],
    )
    return ikb
