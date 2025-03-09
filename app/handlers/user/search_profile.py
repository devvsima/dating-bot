from random import shuffle

from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from app.handlers.bot_utils import complaint_to_profile, menu, send_profile
from app.handlers.msg_text import msg_text
from app.keyboards.default.base import search_kb
from app.keyboards.inline.archive import check_archive_ikb
from app.others.states import Search
from app.routers import user_router as router
from database.models import UserModel
from database.services import Match, Profile
from database.services.search import search_profiles

from .cancel import cancel_command


@router.message(StateFilter(None), F.text == "🔍")
async def _search_command(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """Бот подбирает анкеты, соответствующие предпочтениям пользователя, и предлагает их"""
    await message.answer(msg_text.SEARCH, reply_markup=search_kb)

    if profile_list := await search_profiles(session, user.profile):
        await state.set_state(Search.search)
        await state.update_data(ids=profile_list)

        profile = await Profile.get(session, profile_list[0])
        await send_profile(message.from_user.id, profile)
    else:
        await message.answer(msg_text.INVALID_PROFILE_SEARCH)
        await menu(message.from_user.id)


@router.message(StateFilter(Search.search), F.text.in_(("❤️", "👎", "💢")))
async def _search_profile(message: types.Message, state: FSMContext, session) -> None:
    """
    Пользователь может взаимодействовать с анкетами, предложенными ботом,
    ставя лайк или дизлайк.
    Также доступна функция жалобы на анкеты, содержащие нежелательный контент.
    Все жалобы отправляются в модераторскую группу, если она указана в настройках.
    """
    data = await state.get_data()
    profile_list = data.get("ids", [])
    profile = await Profile.get(session, profile_list[0])

    if message.text == "❤️":
        await Match.create(session, message.from_user.id, profile.user_id)
        await message.bot.send_message(
            chat_id=profile.user_id,
            text=msg_text.LIKE_PROFILE,
            reply_markup=check_archive_ikb(),
        )
    elif message.text == "💢":
        await message.answer(msg_text.REPORT_TO_PROFILE)
        await complaint_to_profile(
            session=session,
            user=message.from_user,
            profile=profile,
        )
    profile_list.pop(0)
    if profile_list:
        profile = await Profile.get(session, profile_list[0])
        await state.update_data(ids=profile_list)
        await send_profile(message.from_user.id, profile)
    else:
        await message.answer(msg_text.EMPTY_PROFILE_SEARCH)
        await cancel_command(message, state)
