from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from loader import _


def block_user_ikb(user) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        resize_keyboard=True,
        
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("☠️ Заблокировать пользователя {}").format(user.username), callback_data=f"block_user_{user.id}"),
            ],
            [
                InlineKeyboardButton(text=_("Отклонить"), callback_data="..."),
            ],
        ],
        
    )
    return ikb