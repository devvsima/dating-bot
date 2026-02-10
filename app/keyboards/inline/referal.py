from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from core.loader import i18n

REF_LINK = "https://t.me/your_bot?start=ref_123"


def referal_ikb(url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👥 Пригласить друзей", switch_inline_query=f"Заходи в бота 👇\n{url}"
                )
            ]
        ]
    )
