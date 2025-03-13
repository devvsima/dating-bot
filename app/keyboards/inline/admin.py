from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.filters.kb_filter import BlockUserCallback
from loader import _


def stats_ikb(text: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=text, callback_data=f"stats_{text}")
    return builder.as_markup()


def block_user_ikb(user_id: int, username: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="☠️ Block user {}".format(username),
        callback_data=BlockUserCallback(user_id=user_id),
    )
    builder.button(
        text="Reject",
        callback_data=BlockUserCallback(user_id=None),
    )

    return builder.as_markup()
