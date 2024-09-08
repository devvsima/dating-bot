from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from utils.logging import logger

from database.service.likes import get_profile_likes, del_like, set_new_like
from database.service.search import elastic_search_user_ids, get_profile

from app.handlers.msg_text import msg_text
from app.states.search_state import Search
from app.states.like_responce import LikeResponse
from app.keyboards.default.choise import search_kb
# from app.keyboards.inline.search import check_like_ikb
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
            

# @dp.callback_query_handler(Text(startswith="check_"), state="*")
@dp.message_handler(Text("🗄"), state="*")
async def like_profile(message: types.Message, state: FSMContext):
    await message.answer(text=msg_text.SEARCH, reply_markup=search_kb())
    await LikeResponse.response.set()
    liker_ids = get_profile_likes(int(message.from_user.id))
    
    if not liker_ids:
        await message.answer(msg_text.LIKE_ARCHIVE)
        await _cancel_command(message, state)
        return
    else:
        await state.update_data(ids=liker_ids)
        profile = await get_profile(liker_ids[0])
        await send_profile(message, profile)
        


@dp.message_handler(Text(["❤️", "👎"]), state=LikeResponse.response)
async def _like_response(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        ids = data.get('ids')
        profile = await get_profile(ids[0])
            
        # logger.info(profile)
        if message.text == "❤️":
            del_like(message.from_user.id, profile.id)
            await bot.send_message(chat_id=message.from_user.id, text=msg_text.LIKE_ACCEPT.format(profile.id, profile.name))
            await bot.send_message(chat_id=profile.id, text=msg_text.LIKE_ACCEPT.format(message.from_user.id, message.from_user.full_name))
        elif message.text == "👎":
            del_like(message.from_user.id, profile.id)
        
        del data['ids'][0]  # Удаляем первый элемент из списка
        if not ids:
            await message.answer(msg_text.EMPTY_PROFILE_SEARCH)
            await _cancel_command(message, state)
            return
        else:
            profile = await get_profile(ids[0])
            await send_profile(message, profile)
        