from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from random import shuffle

from app.routers import user_router as router

from database.models.profile import Profile
from database.service.likes import set_new_like
from database.service.search import elastic_search_user_ids, get_profile

from app.others.states import Search
from app.keyboards.default.base import search_kb
from app.keyboards.inline.archive import check_archive_ikb

from app.handlers.bot_utils import menu, send_profile, report_to_profile
from app.handlers.msg_text import msg_text
from .cancel import cancel_command


@router.message(F.text == "🔍", StateFilter(None))
async def _search_command(message: types.Message, state: FSMContext) -> None:
    """Начинает поиск анкет"""
    await message.answer(msg_text.SEARCH, reply_markup= search_kb)

    ids = await elastic_search_user_ids(message.from_user.id)
    if not ids:
        await message.answer(msg_text.INVALID_PROFILE_SEARCH)
        await menu(message.from_user.id)
        return

    shuffle(ids)

    await state.set_state(Search.search)
    await state.update_data(ids=ids)

    profile = await get_profile(ids[0])
    await send_profile(message.from_user.id, profile)


@router.message(Search.search, F.text.in_(["❤️", "👎", "💢"]))
async def _search_profile(message: types.Message, state: FSMContext) -> None:
    """Свайпы анкет"""
    data: dict = await state.get_data()
    ids: list = data.get("ids", [])
    profile: Profile = await get_profile(ids[0])

    if message.text == "❤️":
        await set_new_like(message.from_user.id, profile.user_id)
        await message.bot.send_message(
            chat_id = profile.user_id.id,
            text = msg_text.LIKE_PROFILE,
            reply_markup = check_archive_ikb(),
        )
    elif message.text == "💢":
        await message.answer(msg_text.REPORT_TO_PROFILE) 
        await report_to_profile(message.from_user, profile)

    ids.pop(0)

    if not ids:
        await message.answer(msg_text.EMPTY_PROFILE_SEARCH)
        await cancel_command(message, state)
        return

    await state.update_data(ids=ids)

    profile: Profile = await get_profile(ids[0])
    await send_profile(message.from_user.id, profile)
