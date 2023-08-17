from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def start_kb():
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="🇺🇦Українська"),
            ],
            [
                KeyboardButton(text="🇬🇧English"),
            ],
            [
                KeyboardButton(text="🏳️Русский"),
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
                KeyboardButton(text="Парни"),
                KeyboardButton(text="Девушки"),
                KeyboardButton(text="Все"),
            ],
        ],
    )
    return kb


def base_selection():
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="ㅤ🔍ㅤ"),
                KeyboardButton(text="ㅤ👤ㅤ"),
                KeyboardButton(text="ㅤ❌ㅤ"),
                KeyboardButton(text="ㅤ✉️ㅤ"),
            ],
        ],
    )
    return kb


def comm_profile():
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="🔄ㅤ"),
                KeyboardButton(text="🖼ㅤ"),
                KeyboardButton(text="✍️ㅤ"),
                KeyboardButton(text="🔍ㅤ"),
            ],
        ],
    )
    return kb
