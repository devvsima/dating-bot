from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
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

# async def contact_keyboard() -> ReplyKeyboardMarkup:
#     kb = ReplyKeyboardMarkup(
#         resize_keyboard=True,
#         keyboard=[
#             [
#                 KeyboardButton(text=_("📱 Отправить"), request_contact=True)
#             ],
#         ],
#     )
#     return kb
