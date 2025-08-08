import html
from ast import Match
from cProfile import Profile

from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.business.profile_service import complaint_to_profile, send_profile_with_dist
from app.constans import EFFECTS_DICTIONARY
from app.handlers.common.start import start_command
from app.keyboards.default.base import match_kb
from app.keyboards.default.report import report_kb
from app.routers import dating_router
from app.states.default import LikeResponse
from app.text import message_text as mt
from database.models import UserModel
from database.services import Match, Profile, User
from loader import bot


@dating_router.message(StateFilter(None), F.text == "📭")
async def match_archive(
    message: types.Message, state: FSMContext, user: UserModel, session: AsyncSession
) -> None:
    """Архив лайков анкеты пользовтеля"""
    await state.set_state(LikeResponse.response)
    await User.update(
        session,
        id=user.id,
        username=message.from_user.username,
    )  # needs to be redone

    if liker_ids := await Match.get_user_matchs(session, message.from_user.id):
        text = mt.ARCHIVE_SEARCH.format(len(liker_ids))
        await message.answer(text=text, reply_markup=match_kb)

        await state.update_data(ids=liker_ids)
        profile = await Profile.get(session, liker_ids[0])
        match_data = await Match.get(session, user.id, profile.id)
        await send_profile_with_dist(user=user, profile=profile, session=session)
        if match_data.message:
            await message.answer(mt.MESSAGE_TO_YOU.format(match_data.message))
    else:
        await message.answer(mt.LIKE_ARCHIVE)
        await (message, state)


@dating_router.callback_query(StateFilter("*"), F.data == "archive")
async def _match_atchive_callback(
    callback: types.CallbackQuery, state: FSMContext, user: UserModel, session: AsyncSession
) -> None:
    """Архив лайков анкеты пользовтеля"""
    await state.set_state(LikeResponse.response)
    await User.update(
        session,
        id=user.id,
        username=callback.from_user.username,
    )  # needs to be redone
    await callback.message.answer(text=mt.SEARCH, reply_markup=match_kb)
    await callback.answer()

    if liker_ids := await Match.get_user_matchs(session, callback.from_user.id):
        await state.update_data(ids=liker_ids)
        profile = await Profile.get(session, liker_ids[0])
        match_data = await Match.get(session, user.id, profile.id)
        await send_profile_with_dist(user=user, profile=profile, session=session)
        if match_data.message:
            await callback.message.answer(mt.MESSAGE_TO_YOU.format(match_data.message))
    else:
        await callback.message.answer(mt.LIKE_ARCHIVE)
        await start_command(callback.message, state, user)


@dating_router.message(
    StateFilter(LikeResponse.response), F.text.in_(("❤️", "👎", "💢", "↩️", "🔞", "💰", "🔫"))
)
async def _match_response(
    message: types.Message, state: FSMContext, user: UserModel, session: AsyncSession
) -> None:
    """'Свайпы' людей которые лайкнули анкету пользователя"""
    data = await state.get_data()
    ids = data.get("ids")

    another_user = await User.get_with_profile(session, ids[0])

    if message.text == "❤️":
        effect_id = EFFECTS_DICTIONARY["🎉"]
        """Отправка пользователю который ответил на лайк"""
        link = generate_user_link(id=another_user.id, username=another_user.username)
        text = mt.LIKE_ACCEPT(another_user.language).format(
            link, html.escape(another_user.profile.name)
        )
        try:
            await bot.send_message(chat_id=user.id, text=text, message_effect_id=effect_id)
        except:
            ...
        """Отправка пользователю которому ответили на лайк"""
        link = generate_user_link(id=user.id, username=user.username)
        text = mt.LIKE_ACCEPT_ALERT(user.language).format(link, html.escape(user.profile.name))
        try:
            await bot.send_message(chat_id=another_user.id, text=text, message_effect_id=effect_id)
        except:
            ...
    elif message.text == "👎":
        pass
    elif message.text == "💢":
        await message.answer(mt.COMPLAINT, reply_markup=report_kb())
        return
    elif message.text in ("🔞", "💰", "🔫"):
        await message.answer(mt.REPORT_TO_PROFILE, reply_markup=match_kb)
        await complaint_to_profile(
            complainant=user,
            reason=message.text,
            complaint_user=another_user,
            session=session,
        )
    elif message.text == "↩️":
        await message.answer(mt.SEARCH, reply_markup=match_kb)
    await Match.delete(session, user.id, another_user.id)

    ids.pop(0)
    await state.update_data(ids=ids)
    if ids:
        profile = await Profile.get(session, ids[0])
        match_data = await Match.get(session, user.id, profile.id)
        await send_profile_with_dist(user=user, profile=profile, session=session)
        if match_data.message:
            await message.answer(mt.MESSAGE_TO_YOU.format(match_data.message))
    else:
        await message.answer(mt.EMPTY_PROFILE_SEARCH)
        await start_command(message, state, user)


def generate_user_link(id: int, username: str = None) -> str:
    """
    Генерирует ссылку на пользователя
    Если указан username, создается ссылка https://t.me/username,
    иначе используется tg://user?id=id.
    """
    if username:
        return f"https://t.me/{username}"
    return f"tg://user?id={id}"
