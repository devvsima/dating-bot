from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.filters.kb_filter import BlockUserCallback
from loader import _


def block_user_ikb(user_id: int, username: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=_("☠️ Заблокировать пользователя {}").format(username),
        callback_data=BlockUserCallback(user_id=user_id),
    )
    builder.button(
        text=_("Отклонить"),
        callback_data=BlockUserCallback(user_id=None),
    )

    return builder.as_markup()
