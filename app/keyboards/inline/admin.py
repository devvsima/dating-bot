from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.filters.kb_filter import BlockUserCallback, StatsCallback
from loader import _


def stats_ikb(current_type: str = "User") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # Добавляем кнопки для всех типов статистики
    stats_types = [("👤 Users", "User"), ("📂 Profiles", "Profile"), ("📊 Referrals", "Referral")]

    for text, callback_type in stats_types:
        # Добавляем эмодзи активности для текущего типа
        if callback_type == current_type:
            text = f"🔹 {text}"
        builder.button(text=text, callback_data=StatsCallback(type=callback_type))

    builder.adjust(2)  # Размещаем кнопки в ряд
    return builder.as_markup()


def block_user_ikb(id: int, username: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="☠️ Block user {}".format(username),
        callback_data=BlockUserCallback(id=id, username=username, ban=True),
    )
    builder.button(
        text="Dismiss",
        callback_data=BlockUserCallback(id=id, username=username, ban=False),
    )

    return builder.as_markup()
