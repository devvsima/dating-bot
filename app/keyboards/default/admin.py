from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from loader import _


def admin_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=_("📊 Статистика")),
            ],
            [
                KeyboardButton(text=_("👤 Пользователи")),
            ],
            [
                KeyboardButton(text=_("📩 Рассылка")),
            ],

        ],
        one_time_keyboard=True,

    )
    return kb


def user_ban_or_unban_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
            KeyboardButton(text=_(f"⚔️ Забанить пользователей")),
            ],
            [
            KeyboardButton(text=_("💊 Разбанить пользователей")),

            ],
        ],
        one_time_keyboard=True,
    )
    return kb