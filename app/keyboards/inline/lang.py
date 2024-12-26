from aiogram.types import (
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from loader import _

def lang_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        resize_keyboard=True,
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Русский", callback_data="ru"),
            ],
            [
                InlineKeyboardButton(text="Українська", callback_data="uk"),
            ],
            [
                InlineKeyboardButton(text="English", callback_data="en"),
            ],
        ],
    )
    return ikb