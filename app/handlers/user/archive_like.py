from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from app.handlers.bot_utils import generate_user_link, sending_user_contact
from app.handlers.message_text import user_message_text as umt
from app.keyboards.default.base import arhive_search_kb
from app.others.states import DisableProfile, LikeResponse
from app.routers import user_router as router
from database.models import UserModel
from database.services import Match, Profile, User

from .cancel import cancel_command
from .profile import send_profile


@router.message(F.text == "🗄", StateFilter("*"))
async def like_profile(message: types.Message, state: FSMContext, user: UserModel, session) -> None:
    """Архив лайков анкеты пользовтеля"""
    if await state.get_state() == DisableProfile.waiting:
        return
    await User.update_username(session, user, message.from_user.username)  # needs to be redone
    await message.answer(text=umt.SEARCH, reply_markup=arhive_search_kb)
    await state.set_state(LikeResponse.response)

    if liker_ids := await Match.get_all(session, message.from_user.id):
        await state.update_data(ids=liker_ids)
        profile = await Profile.get(session, liker_ids[0])
        await send_profile(message.from_user.id, profile)
    else:
        await message.answer(umt.LIKE_ARCHIVE)
        await cancel_command(message, state)


@router.callback_query(F.data == "archive", StateFilter("*"))
async def _like_profile(
    callback: types.CallbackQuery, state: FSMContext, user: UserModel, session
) -> None:
    """Архив лайков анкеты пользовтеля"""
    if await state.get_state() == DisableProfile.waiting:
        return
    await state.set_state(LikeResponse.response)
    await User.update_username(session, user, callback.from_user.username)  # needs to be redone
    await callback.message.answer(text=umt.SEARCH, reply_markup=arhive_search_kb)
    await callback.answer()

    if liker_ids := await Match.get_all(session, callback.from_user.id):
        await state.update_data(ids=liker_ids)
        profile = await Profile.get(session, liker_ids[0])
        await send_profile(callback.from_user.id, profile)
    else:
        await callback.message.answer(umt.LIKE_ARCHIVE)
        await cancel_command(callback.message, state)


@router.message(LikeResponse.response, F.text.in_(("❤️", "👎")))
async def _like_response(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """'Свайпы' людей которые лайкнули анкету пользователя"""
    data = await state.get_data()
    ids = data.get("ids")

    another_user = await User.get_with_profile(session, ids[0])

    if message.text == "❤️":
        """Отправка пользователю который ответил на лайк"""
        link = generate_user_link(user_id=another_user.id, username=another_user.username)
        await sending_user_contact(
            chat_id=user.id,
            name=another_user.profile.name,
            language=user.language,
            user_link=link,
        )

        """Отправка пользователю которому ответили на лайк"""
        link = generate_user_link(user_id=user.id, username=user.username)
        await sending_user_contact(
            chat_id=another_user.id,
            name=user.profile.name,
            language=another_user.language,
            user_link=link,
        )

    await Match.delete(session, user.id, another_user.id)

    ids.pop(0)
    await state.update_data(ids=ids)
    if ids:
        profile = await Profile.get(session, ids[0])
        await send_profile(user.id, profile)
    else:
        await message.answer(umt.EMPTY_PROFILE_SEARCH)
        await cancel_command(message, state)
