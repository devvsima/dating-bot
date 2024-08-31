from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from utils.logging import logger

from app.handlers import msg_text


@dp.message_handler(Text("🗄"))
async def _search_command(message: types.Message, state: FSMContext):
    from database.service.likes import get_profile_likes
    
    
    await message.answer(f"Тебя лайкнуло - {get_profile_likes(message.from_user.id)}")