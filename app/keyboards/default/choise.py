from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from loader import _


def menu_kb():
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="🔍"),
                KeyboardButton(text="👤"),
                KeyboardButton(text="🗄"),
            ],
            [
                KeyboardButton(text="✉️"),
            ],
        ],
    )
    return kb


def profile_kb():
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="🔄"),
                KeyboardButton(text="🖼"),
                KeyboardButton(text="✍️"),
                KeyboardButton(text="❌"),
            ],
            [
                KeyboardButton(text="🔍"),

            ],
        ],
    )
    return kb

def search_kb():
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="❤️"),
                KeyboardButton(text="👎"),
                KeyboardButton(text="💤"),

            ],
        ],
    )
    return kb