from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


def report_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
            keyboard=[
            [
                KeyboardButton(text=_("🔞 Неприличный материал")),
            ],
            [
                KeyboardButton(text=_("💰 Реклама")),
            ],
            [
                KeyboardButton(text=_("🔫 Другое")),
            ],
        ],
    )
    return kb

