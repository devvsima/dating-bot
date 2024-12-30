from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from loader import _

def check_archive_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        resize_keyboard=True,
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Посмотреть"), callback_data="archive"),
            ],
        ],
    )
    return ikb

