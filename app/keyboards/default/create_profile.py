from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from loader import _


def start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=_("Создать анкету")),
            ],
        ],
    )
    return kb


def gender_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text=_("Парень")), KeyboardButton(text=_("Девушка"))],
        ],
    )
    return kb


def find_gender_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=_("Парней")),
                KeyboardButton(text=_("Девушек")),
                KeyboardButton(text=_("Всех")),
            ],
        ],
    )
    return kb
