from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from loader import _


def webapp_test_kb():
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=_("🚀 Открыть WebApp")),
            ],
        ],
    )
    return kb
