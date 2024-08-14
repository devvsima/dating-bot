from aiogram.types import (
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from loader import _

def check_like_ikb(user_id):
    ikb = InlineKeyboardMarkup(
        resize_keyboard=True,
        inline_keyboard=[
            [
                InlineKeyboardButton(text=("Посмотреть👀"), callback_data=f"check_{user_id}"),
            ],
        ],
    )
    return ikb
