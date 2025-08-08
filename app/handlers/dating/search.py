from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

import app.filters.create_profile_filtres as filters
from app.business.dating_service import send_user_like_alert
from app.business.menu_service import menu
from app.business.profile_service import complaint_to_profile, send_profile_with_dist
from app.handlers.common.start import start_command
from app.keyboards.default.base import return_to_menu_kb, search_kb
from app.keyboards.default.report import report_kb
from app.routers import dating_router
from app.states.default import Search
from app.text import message_text as mt
from database.models import UserModel
from database.services import Match, Profile, User
from database.services.search import search_profiles


@dating_router.message(StateFilter(None), F.text == "🔍")
async def _search_command(
    message: types.Message, state: FSMContext, user: UserModel, session: AsyncSession
) -> None:
    """Бот подбирает анкеты, соответствующие предпочтениям пользователя, и предлагает их"""
    await message.answer(mt.SEARCH, reply_markup=search_kb)

    if profile_list := await search_profiles(session, user.profile):
        await state.set_state(Search.search)
        await state.update_data(ids=profile_list)

        another_profile = await Profile.get(session, profile_list[0])
        await send_profile_with_dist(user=user, profile=another_profile, session=session)

    else:
        await message.answer(mt.INVALID_PROFILE_SEARCH)
        await menu(message.from_user.id)


@dating_router.message(
    StateFilter(Search.search),
    F.text.in_(("❤️", "👎", "💢", "📩")),
)
async def _search_profile(
    message: types.Message, state: FSMContext, user: UserModel, session: AsyncSession
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
        await like_profile(
            session=session,
            message=message,
            another_user=another_user,
        )
    elif message.text == "👎":
        pass
    elif message.text == "📩":
        await state.set_state(Search.message)
        await message.answer(mt.MAILING_TO_USER, reply_markup=return_to_menu_kb)
        return

    if message.text == "💢":
        await message.answer(mt.COMPLAINT, reply_markup=report_kb())
        return
    await next_profile(session, message, profile_list, user, state)


@dating_router.message(StateFilter(Search.search), F.text.in_(("🔞", "💰", "🔫", "↩️")))
async def _search_profile_report(
    message: types.Message, state: FSMContext, user: UserModel, session: AsyncSession
) -> None:
    """Пользователь может отправить жалобу на анкету, если она содержит нежелательный контент."""
    data = await state.get_data()
    profile_list = data.get("ids", [])
    another_user = await User.get_with_profile(session, profile_list[0])

    if message.text in ("🔞", "💰", "🔫"):
        await message.answer(mt.REPORT_TO_PROFILE, reply_markup=search_kb)
        await complaint_to_profile(
            complainant=user,
            reason=message.text,
            complaint_user=another_user,
            session=session,
        )
    elif message.text == "↩️":
        await message.answer(mt.SEARCH, reply_markup=search_kb)
    await next_profile(session, message, profile_list, user, state)


@dating_router.message(StateFilter(Search.message), F.text, filters.IsMessageToUser())
async def _search_profile_mailing_(
    message: types.Message, state: FSMContext, user: UserModel, session: AsyncSession
) -> None:
    """Ловит сообщение которые пользователь отправляет в ответ на анкету"""
    data = await state.get_data()
    profile_list = data.get("ids", [])
    another_user = await User.get_with_profile(session, profile_list[0])
    await state.set_state(Search.search)

    if message.text == "↩️":
        await message.answer(mt.CANNCELED_LETTER, reply_markup=search_kb)
        await send_profile_with_dist(user=user, profile=another_user.profile, session=session)

        return
    await like_profile(
        session=session,
        message=message,
        another_user=another_user,
        mail_text=message.text,
    )
    await message.answer(mt.MAILING_LIKE, reply_markup=search_kb)
    await next_profile(session, message, profile_list, user, state)


@dating_router.message(StateFilter(Search.message))
async def _search_profile_mailing_error(message: types.Message) -> None:
    """Ловит ошибку, если пользователь отправляет сообщение не по шаблону"""
    await message.answer(mt.INVALID_MAILING_TO_USER)


async def next_profile(
    session: AsyncSession,
    message: types.Message,
    profile_list: UserModel,
    user: UserModel,
    state: FSMContext,
):
    profile_list.pop(0)
    if profile_list:
        profile = await Profile.get(session, profile_list[0])
        await state.update_data(ids=profile_list)
        await send_profile_with_dist(user=user, profile=profile, session=session)
    else:
        await message.answer(mt.EMPTY_PROFILE_SEARCH)
        await start_command(message, state, user)


async def like_profile(
    session: AsyncSession,
    message: types.Message,
    another_user: UserModel,
    mail_text: str | None = None,
):
    is_create = await Match.create(session, message.from_user.id, another_user.id, mail_text)

    if is_create:
        matchs_count = len(await Match.get_user_matchs(session, message.from_user.id))
        if matchs_count == 1 or matchs_count % 3 == 0:
            await send_user_like_alert(session, another_user)
