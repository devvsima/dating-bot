import html

from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from app.handlers.bot_utils import generate_user_link, send_message_with_effect
from app.handlers.message_text import user_message_text as umt
from app.keyboards.default.base import arhive_search_kb
from app.others.states import LikeResponse
from app.routers import dating_router
from database.models import UserModel
from database.services import Match, Profile, User

from ..common.cancel import cancel_command
from .profile import send_profile


@dating_router.message(StateFilter("*"), F.text == "📭")
async def match_archive(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """Архив лайков анкеты пользовтеля"""
    await state.set_state(LikeResponse.response)
    await User.update(
        session,
        id=user.id,
        username=message.from_user.username,
    )  # needs to be redone

    if liker_ids := await Match.get_user_matchs(session, message.from_user.id):
        text = umt.ARCHIVE_SEARCH.format(len(liker_ids))
        await message.answer(text=text, reply_markup=arhive_search_kb)

        await state.update_data(ids=liker_ids)
        profile = await Profile.get(session, liker_ids[0])
        await send_profile(message.from_user.id, profile)
    else:
        await message.answer(umt.LIKE_ARCHIVE)
        await cancel_command(message, state)


@dating_router.callback_query(StateFilter("*"), F.data == "archive")
async def _match_atchive_callback(
    callback: types.CallbackQuery, state: FSMContext, user: UserModel, session
) -> None:
    """Архив лайков анкеты пользовтеля"""
    await state.set_state(LikeResponse.response)
    await User.update(
        session,
        id=user.id,
        username=callback.from_user.username,
    )  # needs to be redone
    await callback.message.answer(text=umt.SEARCH, reply_markup=arhive_search_kb)
    await callback.answer()

    if liker_ids := await Match.get_user_matchs(session, callback.from_user.id):
        await state.update_data(ids=liker_ids)
        profile = await Profile.get(session, liker_ids[0])
        await send_profile(callback.from_user.id, profile)
    else:
        await callback.message.answer(umt.LIKE_ARCHIVE)
        await cancel_command(callback.message, state)


@dating_router.message(StateFilter(LikeResponse.response), F.text.in_(("❤️", "👎")))
async def _match_response(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """'Свайпы' людей которые лайкнули анкету пользователя"""
    data = await state.get_data()
    ids = data.get("ids")

    another_user = await User.get_with_profile(session, ids[0])

    if message.text == "❤️":
        """Отправка пользователю который ответил на лайк"""
        link = generate_user_link(id=another_user.id, username=another_user.username)
        text = umt.LIKE_ACCEPT(another_user.language).format(
            link, html.escape(another_user.profile.name)
        )
        await send_message_with_effect(chat_id=user.id, text=text)

        """Отправка пользователю которому ответили на лайк"""
        link = generate_user_link(id=user.id, username=user.username)
        text = umt.LIKE_ACCEPT_ALERT(user.language).format(link, html.escape(user.profile.name))
        await send_message_with_effect(chat_id=another_user.id, text=text)

    await Match.delete(session, user.id, another_user.id)

    ids.pop(0)
    await state.update_data(ids=ids)
    if ids:
        profile = await Profile.get(session, ids[0])
        await send_profile(user.id, profile)
    else:
        await message.answer(umt.EMPTY_PROFILE_SEARCH)
        await cancel_command(message, state)
