from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from loader import _


def compleint_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text="🔞"), KeyboardButton(text="💰"), KeyboardButton(text="🔫")],
            [KeyboardButton(text="↩️")],
        ],
    )
    return kb
