import os

from aiogram import F, types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from app.handlers.msg_text import msg_text
from app.routers import admin_router as router
from database.services.stat import get_profile_statistics, get_user_statistics
from utils.graphs import get_or_create_registration_graph


@router.message(Command("stats"), StateFilter(None))
@router.message(F.text.in_(["📊 Статистика", "📊 Statistics"]), StateFilter(None))
async def _stats_command(message: types.Message, session) -> None:
    """
    Отправляет администратору график регистрации пользователей
    и статистику пользователей в БД
    """
    profile_stats = await get_profile_statistics(session)
    users_stats = await get_user_statistics(session)
    graph_path = await get_or_create_registration_graph(session)
    photo = types.FSInputFile(graph_path)

    text = msg_text.USERS_STATS.format(
        users_stats["count"],
        users_stats["banned_count"],
        profile_stats["count"],
        profile_stats["inactive_profile"],
        profile_stats["male_count"],
        profile_stats["female_count"],
    )

    await message.answer_photo(photo, text)

    # Удаляем временный файл
    os.remove(graph_path)
