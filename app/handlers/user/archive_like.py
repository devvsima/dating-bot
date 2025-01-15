from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from utils.logging import logger

from database.service.likes import get_profile_likes, del_like
from database.service.profile import get_profile

from .profile import send_profile
from .cancel import cancel_command
from app.handlers.msg_text import msg_text
from app.states.like_responce import LikeResponse
from app.keyboards.default import search_kb 


@dp.message_handler(Text("🗄"), state="*")
async def like_profile(message: types.Message, state: FSMContext) -> None:
    await message.answer(text=msg_text.SEARCH, reply_markup=search_kb())
    await LikeResponse.response.set()
    liker_ids = get_profile_likes(message.from_user.id)
    if not liker_ids:
        await message.answer(msg_text.LIKE_ARCHIVE)
        await cancel_command(message, state)
        return
    else:
        await state.update_data(ids=liker_ids)
        profile = await get_profile(liker_ids[0])
        await send_profile(message.from_user.id, profile)
        

@dp.callback_query_handler(Text("archive"), state="*")
async def _like_profile(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(text=msg_text.SEARCH, reply_markup=search_kb())
    await LikeResponse.response.set()
    liker_ids = get_profile_likes(int(callback.from_user.id))
    logger.info(liker_ids)
    if not liker_ids:
        await callback.message.answer(msg_text.LIKE_ARCHIVE)
        await cancel_command(callback.message, state)
        return
    else:
        await state.update_data(ids=liker_ids)
        profile = await get_profile(liker_ids[0])
        await send_profile(callback.from_user.id, profile)
    
        
@dp.message_handler(Text(["❤️", "👎"]), state=LikeResponse.response)
async def _like_response(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        ids = data.get('ids')
        profile = await get_profile(ids[0])
        
        username_url = "https://t.me/{}"
        id_url = "tg://user?id={}"
                
        if message.text == "❤️":
            """Отправка пользователю которому ответили на лайк"""
            url = id_url.format(message.from_user.id)
            if message.from_user.username:
                url = username_url.format(message.from_user.username)
                
            await bot.send_message(
                chat_id=profile.user_id, 
                text=msg_text.LIKE_ACCEPT.format(url, message.from_user.full_name)
                )
            
            """Отправка пользователю который ответил на лайк"""
            url = id_url.format(profile.user_id)
            if profile.user_id.username:
                url = username_url.format(profile.user_id.username)
                
            await bot.send_message(
                chat_id=message.from_user.id,
                text=msg_text.LIKE_ACCEPT.format(url,profile.name ))
            
        elif message.text == "👎":
            pass
        del_like(message.from_user.id, profile.user_id)
        
        del data['ids'][0] 
        if not ids:
            await message.answer(msg_text.EMPTY_PROFILE_SEARCH)
            await cancel_command(message, state)
            return
        else:
            profile = await get_profile(ids[0])
            await send_profile(message.from_user.id, profile)
        