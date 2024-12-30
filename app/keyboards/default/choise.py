from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def menu_kb() -> ReplyKeyboardMarkup:
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
        one_time_keyboard=True,

    )
    return kb


def profile_kb() -> ReplyKeyboardMarkup:
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
        one_time_keyboard=True,
    )
    return kb

def search_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="❤️"),
                KeyboardButton(text="👎"),
            ],
            [
                KeyboardButton(text="💤"),
                # KeyboardButton(text="💢"),
            ],

        ],
    )
    return kb