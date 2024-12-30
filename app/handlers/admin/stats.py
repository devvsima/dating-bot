from aiogram import types
from aiogram.dispatcher.filters import Text, Command
from app.filters.admin import IsAdmin

from loader import dp
from utils.graphs import get_or_create_registration_graph

from database.service.stats import get_profile_stats, get_users_stats

from app.handlers.msg_text import msg_text

        
@dp.message_handler(IsAdmin(), Text("📊 Статистика"))
async def _stats_command(message: types.Message) -> None:
    """Отправляет администратору график регистрации пользователей и статистику пользователей в БД"""
    profile_stats = get_profile_stats()
    graph_path = get_or_create_registration_graph()
    text = msg_text.USERS_STATS.format(get_users_stats(), profile_stats['users_count'], profile_stats['male_count'], profile_stats['female_count'])
    with open(graph_path, "rb") as photo:
        await message.answer_photo(photo, text)
