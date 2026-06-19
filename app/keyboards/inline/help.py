from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from core.loader import _, tgbot


def help_ikb(language: str) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        resize_keyboard=True,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_("Написать разработчику", locale=language), url="https://t.me/devvsima"
                )
            ],
            [
                InlineKeyboardButton(
                    text=_("Официальный канал", locale=language), url=tgbot.BOT_CHANNEL_URL
                )
            ],
            [
                InlineKeyboardButton(
                    style="success",
                    text=_("Поддержать проект", locale=language),
                    callback_data="donate",
                )
            ],
        ],
    )
    return ikb
