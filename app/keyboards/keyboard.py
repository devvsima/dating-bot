from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from loader import _

def start_kb():
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="Українська"),
            ],
            [
                KeyboardButton(text="English"),
            ],
            [
                KeyboardButton(text="Русский"),
            ],
        ],
    )
    return kb


def base_kb():
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="/create"),
            ],
        ],
    )
    return kb


def cancel_kb():
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="/cancel"),
            ],
        ],
    )
    return kb


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


def base_selection():
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="🔍"),
                KeyboardButton(text="👤"),
                KeyboardButton(text="❌"),
                KeyboardButton(text="✉️"),
            ],
        ],
    )
    return kb


def comm_profile():
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="🔄"),
                KeyboardButton(text="❌"),
                # KeyboardButton(text="🖼"),
                # KeyboardButton(text="✍️"),
                KeyboardButton(text="🔍"),
            ],
        ],
    )
    return kb


def yes_or_not():
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
