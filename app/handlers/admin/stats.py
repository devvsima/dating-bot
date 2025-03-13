import os

from aiogram import F, types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from app.handlers.message_text import admin_message_text as amt
from app.keyboards.inline.admin import stats_ikb
from app.routers import admin_router
from database.services.stats import (
    get_match_statistics,
    get_profile_statistics,
    get_user_statistics,
)
from utils.graphs import get_or_create_registration_graph


@admin_router.message(Command("stats"), StateFilter(None))
@admin_router.message(F.text == "📊 Statistics", StateFilter(None))
async def _stats_command(message: types.Message, session) -> None:
    """Отправляет администратору меню статистики"""
    graph_path = await get_or_create_registration_graph(session)
    photo = types.FSInputFile(graph_path)
    users_stats = await get_user_statistics(session)
    text = amt.USER_STATS.format(
        users_stats["count"],
        users_stats["banned_count"],
        users_stats["total_referrals"],
        users_stats["most_popular_language"],
    )
    await message.answer_photo(photo=photo, caption=text, reply_markup=stats_ikb("Profile"))

    os.remove(graph_path)


@admin_router.callback_query(F.data.startswith("stats"), StateFilter(None))
async def _stats_callback(callback: types.CallbackQuery, session) -> None:
    """Отправляет администратору график и статистику"""
    graph_path = await get_or_create_registration_graph(session)
    photo = types.FSInputFile(graph_path)
    if callback.data == "stats_User":
        users_stats = await get_user_statistics(session)
        text = amt.USER_STATS.format(
            users_stats["count"],
            users_stats["banned_count"],
            users_stats["total_referrals"],
            users_stats["most_popular_language"],
        )
        kb_text = "Profile"
    elif callback.data == "stats_Profile":
        match_stats = await get_match_statistics(session)
        profile_stats = await get_profile_statistics(session)
        text = amt.PROFILE_STATS.format(
            profile_stats["count"],
            profile_stats["inactive_profile"],
            profile_stats["male_count"],
            profile_stats["female_count"],
            match_stats[0],
            profile_stats["average_age"],
            profile_stats["most_popular_city"],
        )
        kb_text = "User"

    await callback.message.edit_media(
        media=types.InputMediaPhoto(media=photo, caption=text), reply_markup=stats_ikb(kb_text)
    )

    os.remove(graph_path)
