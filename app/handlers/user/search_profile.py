from aiogram import types
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher import FSMContext

from random import shuffle

from loader import dp, bot

from database.models.profile import Profile
from database.service.likes import set_new_like
from database.service.search import elastic_search_user_ids, get_profile

from app.states.search_state import Search
from app.keyboards.default.choise import search_kb
from app.keyboards.inline.archive import check_archive_ikb

from app.handlers.bot_utils import menu, send_profile, report_to_profile
from app.handlers.msg_text import msg_text
from .cancel import cancel_command


@dp.message_handler(Text("🔍"))
async def _search_command(message: types.Message, state: FSMContext) -> None:
    """Начинает поиск анкет"""
    await message.answer(msg_text.SEARCH, reply_markup=search_kb())
    async with state.proxy() as data:
        ids = await elastic_search_user_ids(message.from_user.id)
        if not ids:
            await message.answer(msg_text.INVALID_PROFILE_SEARCH)
            await menu(message.from_user.id)
            return
        
        shuffle(ids)
        await Search.search.set()
        await state.update_data(ids=ids)
        
        profile = await get_profile(ids[0])
        await send_profile(message.from_user.id, profile)

@dp.message_handler(Command("report"), state=Search.search)
@dp.message_handler(Text(["❤️","👎"]), state=Search.search)
async def _search_profile(message: types.Message, state: FSMContext) -> None:
    """Свайпы анкет"""
    async with state.proxy() as data:
        ids = data['ids']
        profile: Profile = await get_profile(ids[0])
        
        if message.text == "👎":
            ...
        elif message.text == "❤️":
            set_new_like(message.from_user.id, profile.user_id)
            await bot.send_message(chat_id=profile.user_id, text=msg_text.LIKE_PROFILE, reply_markup=check_archive_ikb())
        elif message.text == "/report":
            await report_to_profile(message.from_user, profile)

        del data["ids"][0]
        if not ids:
            await message.answer(msg_text.EMPTY_PROFILE_SEARCH)
            await cancel_command(message, state)
            return
        profile = await get_profile(ids[0])
        await send_profile(message.from_user.id, profile)