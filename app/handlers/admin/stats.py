from aiogram import F, types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

import os

from app.routers import admin_router as router

from utils.graphs import get_or_create_registration_graph

from database.service.stats import get_profile_stats, get_users_stats

from app.handlers.msg_text import msg_text



@router.message(Command("stats"), StateFilter(None))
@router.message(F.text.in_(["📊 Статистика", "📊 Statistics"]), StateFilter(None))
async def _stats_command(message: types.Message) -> None:
    """Отправляет администратору график регистрации пользователей и статистику пользователей в БД"""
    profile_stats = await get_profile_stats()
    users_stats = await get_users_stats()
    graph_path = await get_or_create_registration_graph()
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