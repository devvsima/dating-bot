from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.filters.kb_filter import BlockUserCallback, StatsCallback
from core.config import webapp
from core.loader import _


def stats_ikb(current_type: str = "User") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    stats_types = [
        ("Users", "User", "5222479682733116859"),  # 👤
        ("Profiles", "Profile", "5220024327239410094"),  # 📂
        ("Referrals", "Referral", "5220139711535816607"),  # 📊
    ]

    for text, callback_type, emoji_id in stats_types:
        if callback_type == current_type:
            text = f"> {text} <"
        builder.button(
            text=text,
            icon_custom_emoji_id=emoji_id,
            callback_data=StatsCallback(type=callback_type),
        )

    builder.adjust(2)
    return builder.as_markup()


def block_user_ikb(complaint_id: int, user_id: int, username: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    emoji_id = "5219958846168012596"
    builder.button(
        text="Block user: {}".format(username),
        icon_custom_emoji_id=emoji_id,
        callback_data=BlockUserCallback(
            complaint_id=complaint_id,
            receiver_id=user_id,
            receiver_username=username,
            ban=True,
        ),
    )
    # Хотелось бы здесь реализовать отправку предупредительного сообщения
    builder.button(
        text="Dismiss",
        callback_data=BlockUserCallback(
            complaint_id=complaint_id,
            receiver_id=user_id,
            receiver_username=username,
            ban=False,
        ),
    )
    # builder.button(text="🌐 Посмотреть профиль", url=f"{webapp.URL}admin/user/{user_id}")

    builder.adjust(1)
    return builder.as_markup()


def check_user_profile(user_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="🌐 Посмотреть профиль",
        web_app=types.WebAppInfo(
            url=f"{webapp.URL}admin/user/{user_id}",
        ),
    )

    builder.adjust(1)
    return builder.as_markup()
