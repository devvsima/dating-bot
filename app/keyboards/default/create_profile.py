from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from loader import _


def gender_kb():
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Я парень"), KeyboardButton(text="Я девушка")],
        ],
    )
    return kb


def find_gender_kb():
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=("Парни")),
                KeyboardButton(text=("Девушки")),
                KeyboardButton(text=("Все")),
            ],
        ],
    )
    return kb




