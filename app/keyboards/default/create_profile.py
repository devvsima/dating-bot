from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


def gender_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text=_("Я парень")), KeyboardButton(text=_("Я девушка"))],
        ],
    )
    return kb


def find_gender_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=_("Парни")),
                KeyboardButton(text=_("Девушки")),
                KeyboardButton(text=_("Все")),
            ],
        ],
    )
    return kb

def suggest_previous_options_kb(text: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=text),
            ],
        ],
    )
    return kb




