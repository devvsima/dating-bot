from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from utils.logging import logger

from database.service.profile import elastic_search_user_ids, get_profile

from app.states.search_state import Search
from app.keyboards.default.choise import search_kb
from app.keyboards.inline.search import check_like_ikb
from .cancel import _cancel_command
from .profile import _profile_command, send_profile

from random import shuffle

from app.handlers import msg_text

@dp.message_handler(Text("🗄"))
async def _search_command(message: types.Message, state: FSMContext):
    from database.service.likes import get_profile_likes
    
    
    await message.answer(f"Тебя лайкнуло - {get_profile_likes(message.from_user.id)}")