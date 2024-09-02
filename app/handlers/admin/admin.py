from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, bot
from data.config import DIR

from database.service.stats import get_profile_stats, get_users_stats

from utils.graphs import create_user_invite_graph

from app.filters.admin import Admin


photo_path = rf'{DIR}/photo/invites_per_user.png'

@dp.message_handler(Admin(), Command("admin"))
async def _stats_command(message: types.Message): 

    create_user_invite_graph(photo_path)
    user_stats = get_profile_stats()

    text = f"👤Users: {get_users_stats()}\n\nProfiles: {user_stats['total_users']}\n🙍‍♂️Man: {user_stats['male_users']} | 🙍‍♀️Woman: {user_stats['female_users']}"
    with open(photo_path, "rb") as photo:
        await message.answer_photo(
            photo,
            text
            )



