from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, bot
from data.config import DIR

from database.service.stats import get_profile_stats, get_users_stats

from utils.graphs import create_user_invite_graph

from app.filters.admin import Admin


@dp.message_handler(Admin(), Command("admin"))
async def _stats_command(message: types.Message):
    await message.answer('ты админ')