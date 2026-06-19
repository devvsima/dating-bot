from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.config import SUPPORT_COST
from core.loader import _


def payment_ikb():
    builder = InlineKeyboardBuilder()
    builder.button(text=_(f"Оплатить {SUPPORT_COST} ⭐️"), pay=True)

    return builder.as_markup()
