from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import _


def block_user_ikb(user_id: int, username: str) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        resize_keyboard=True,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_("☠️ Заблокировать пользователя {}").format(username),
                    callback_data=f"block_user_{user_id}",
                ),
            ],
            [
                InlineKeyboardButton(text=_("Отклонить"), callback_data="..."),
            ],
        ],
    )
    return ikb
