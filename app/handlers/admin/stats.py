from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, bot

from data.config import DIR

photo_path = rf'{DIR}/photo/invites_per_user.png'


@dp.message_handler(Command("stats"))
async def _stats_command(message: types.Message):
    from utils.graphs import create_user_invite_graph
    create_user_invite_graph()
    with open(photo_path, "rb") as photo:
        await message.answer_photo(photo)



