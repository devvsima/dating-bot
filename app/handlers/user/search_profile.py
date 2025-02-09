from random import shuffle

from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from app.handlers.bot_utils import menu, report_to_profile, send_profile
from app.handlers.msg_text import msg_text
from app.keyboards.default.base import search_kb
from app.keyboards.inline.archive import check_archive_ikb
from app.others.states import Search
from app.routers import user_router as router
from database.services import Match, Profile
from database.services.search import search_profiles

from .cancel import cancel_command


@router.message(F.text == "🔍", StateFilter(None))
async def _search_command(message: types.Message, state: FSMContext, session) -> None:
    """Начинает поиск анкет"""
    await message.answer(msg_text.SEARCH, reply_markup=search_kb)

    ids = await search_profiles(session, message.from_user.id)
    if not ids:
        await message.answer(msg_text.INVALID_PROFILE_SEARCH)
        await menu(message.from_user.id)
        return

    shuffle(ids)

    await state.set_state(Search.search)
    await state.update_data(ids=ids)

    profile = await Profile.get(session, ids[0])
    await send_profile(message.from_user.id, profile)


@router.message(Search.search, F.text.in_(["❤️", "👎", "💢"]))
async def _search_profile(message: types.Message, state: FSMContext, session) -> None:
    """Свайпы анкет"""
    data: dict = await state.get_data()
    ids: list = data.get("ids", [])
    profile = await Profile.get(session, ids[0])

    if message.text == "❤️":
        await Match.set_new_like(session, message.from_user.id, profile.user_id)
        await message.bot.send_message(
            chat_id=profile.user_id,
            text=msg_text.LIKE_PROFILE,
            reply_markup=check_archive_ikb(),
        )
    elif message.text == "💢":
        await message.answer(msg_text.REPORT_TO_PROFILE)
        await report_to_profile(
            session=session,
            user=message.from_user,
            profile=profile,
        )

    ids.pop(0)

    if not ids:
        await message.answer(msg_text.EMPTY_PROFILE_SEARCH)
        await cancel_command(message, state)
        return

    await state.update_data(ids=ids)

    profile = await Profile.get(session, ids[0])
    await send_profile(message.from_user.id, profile)
