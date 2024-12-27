from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from loader import _

def delete_profile_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        resize_keyboard=True,
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Да"), callback_data="delete_yes"),
                InlineKeyboardButton(text=_("Нет"), callback_data="delete_no"),
            ],
        ],
    )
    return ikb
