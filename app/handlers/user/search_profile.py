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

@dp.message_handler(Text("🔍"))
async def _search_command(message: types.Message, state: FSMContext):
    await message.answer(msg_text.SEARCH, reply_markup=search_kb())
    async with state.proxy() as data:
        ids = await elastic_search_user_ids(message.from_user.id)
        
        if not ids:
            await message.answer(msg_text.INVALID_PROFILE_SEARCH)
            await _profile_command(message)
            return
        
        await Search.search.set()
        shuffle(ids)
        await state.update_data(ids=ids, index=0)
        
        await _search_profile(message=message, state=state)
        
@dp.message_handler(Text(["❤️","👎"]), state=Search.search)
async def _search_profile(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
    
        ids = data['ids']
        if not ids:
            await message.answer(msg_text.EMPTY_PROFILE_SEARCH)
            await _cancel_command(message, state)
        else:
            profile = await get_profile(ids[0])
            del data["ids"][0]
            
            if message.text == "❤️":
                index = data['index']
                await bot.send_message(
                    chat_id=profile.id,
                    text=msg_text.LIKE_PROFILE,
                    reply_markup=check_like_ikb(message.from_user.id)
                )
            
            await send_profile(message, profile)
            


@dp.callback_query_handler(Text(startswith="check_"), state="*")
async def like_profile(callback: types.CallbackQuery, state: FSMContext):
    profile = await get_profile(int(callback.data.replace("check_", "")))
    await send_profile(callback.message, profile)
    await callback.answer('')