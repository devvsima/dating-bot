from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from app.filters.search import SearchFilter
from app.handlers.bot_utils import (
    complaint_to_profile,
    menu,
    send_profile_with_dist,
    send_user_like_alert,
)
from app.handlers.message_text import user_message_text as umt
from app.keyboards.default.base import search_kb
from app.keyboards.default.report import report_kb
from app.others.states import Search
from app.routers import dating_router
from database.models import UserModel
from database.services import Match, Profile, User
from database.services.search import haversine_distance, search_profiles

from ..common.cancel import cancel_command


@dating_router.message(StateFilter(None), F.text == "🔍")
async def _search_command(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """Бот подбирает анкеты, соответствующие предпочтениям пользователя, и предлагает их"""
    await message.answer(umt.SEARCH, reply_markup=search_kb)

    if profile_list := await search_profiles(session, user.profile):
        await state.set_state(Search.search)
        await state.update_data(ids=profile_list)

        another_profile = await Profile.get(session, profile_list[0])
        await send_profile_with_dist(user, another_profile)

    else:
        await message.answer(umt.INVALID_PROFILE_SEARCH)
        await menu(message.from_user.id)


@dating_router.message(StateFilter(Search.search), SearchFilter())
async def _search_profile(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """
    Пользователь может взаимодействовать с анкетами, предложенными ботом,
    ставя лайк или дизлайк.
    Также доступна функция жалобы на анкеты, содержащие нежелательный контент.
    Все жалобы отправляются в модераторскую группу, если она указана в настройках.
    """
    data = await state.get_data()
    profile_list = data.get("ids", [])
    another_user = await User.get_with_profile(session, profile_list[0])

    if message.text == "❤️":
        is_create = await Match.create(session, message.from_user.id, another_user.id)

        if is_create:
            matchs_count = len(await Match.get_user_matchs(session, message.from_user.id))
            if matchs_count == 1 or matchs_count % 3 == 0:
                await send_user_like_alert(session, another_user)
    elif message.text == "👎":
        pass
    elif message.text == "💢":
        await message.answer(umt.COMPLAINT, reply_markup=report_kb())
        return
    elif message.text in ("🔞", "💰", "🔫"):
        await message.answer(umt.REPORT_TO_PROFILE, reply_markup=search_kb)
        await complaint_to_profile(
            complainant=user,
            reason=message.text,
            complaint_profile=another_user.profile,
        )
    elif message.text == "↩️":
        await message.answer(umt.SEARCH, reply_markup=search_kb)

    profile_list.pop(0)
    if profile_list:
        profile = await Profile.get(session, profile_list[0])
        await state.update_data(ids=profile_list)
        await send_profile_with_dist(user, profile)
    else:
        await message.answer(umt.EMPTY_PROFILE_SEARCH)
        await cancel_command(message, state)
