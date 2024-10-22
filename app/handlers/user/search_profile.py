from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from utils.logging import logger

from database.service.likes import set_new_like
from database.service.search import elastic_search_user_ids, get_profile

from app.handlers.msg_text import msg_text
from app.states.search_state import Search
from app.keyboards.default.choise import search_kb

from .cancel import _cancel_command
from .profile import _profile_command, send_profile

from random import shuffle


@dp.message_handler(Text("🔍"))
async def _search_command(message: types.Message, state: FSMContext):
    await message.answer(msg_text.SEARCH, reply_markup=search_kb())
    async with state.proxy() as data:
        ids = await elastic_search_user_ids(message.from_user.id)
        
        if not ids:
            await message.answer(msg_text.INVALID_PROFILE_SEARCH)
            await _profile_command(message)
            return
        
        shuffle(ids)
        await Search.search.set()
        await state.update_data(ids=ids)
        
        profile = await get_profile(ids[0])
        await send_profile(message, profile)

        
@dp.message_handler(Text(["❤️","👎"]), state=Search.search)
async def _search_profile(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        ids = data['ids']
        profile = await get_profile(ids[0])
        
        if message.text == "❤️":
            set_new_like(message.from_user.id, profile.id)
            await bot.send_message(chat_id=profile.id, text=msg_text.LIKE_PROFILE)
        elif message.text == "👎":
            ...
        
        del data["ids"][0]
        if not ids:
            await message.answer(msg_text.EMPTY_PROFILE_SEARCH)
            await _cancel_command(message, state)
            return
        profile = await get_profile(ids[0])
        await send_profile(message, profile)
            

