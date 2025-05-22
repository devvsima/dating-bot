from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from loader import _


def report_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text="🔞"), KeyboardButton(text="💰"), KeyboardButton(text="🔫")],
            [KeyboardButton(text=_("Отменить жалобу"))],
        ],
    )
    return kb
