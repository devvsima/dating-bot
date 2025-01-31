from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from app.routers import user_router as router

from database.service.likes import get_profile_likes, del_like
from database.service.profile import get_profile
from database.service.users import update_user_username
from database.models.profile import Profile

from .profile import send_profile
from .cancel import cancel_command
from app.handlers.msg_text import msg_text
from app.others.states import DisableProfile, LikeResponse
from app.keyboards.default.base import arhive_search_kb
from app.handlers.bot_utils import sending_user_contact, generate_user_link


@router.message(F.text == "🗄", StateFilter("*"))
async def like_profile(message: types.Message, state: FSMContext) -> None:
    """Архив лайков анкеты пользовтеля"""
    if await state.get_state() == DisableProfile.waiting:
        return
    await update_user_username(message.from_user.id, message.from_user.username)
    await message.answer(
        text=msg_text.SEARCH,
        reply_markup=arhive_search_kb
    )
    await state.set_state(LikeResponse.response)

    if liker_ids := await get_profile_likes(message.from_user.id):
        await state.update_data(ids=liker_ids)
        profile = await get_profile(liker_ids[0])
        await send_profile(message.from_user.id, profile)
    else:
        await message.answer(msg_text.LIKE_ARCHIVE)
        await cancel_command(message, state)


@router.callback_query(F.data == "archive", StateFilter("*"))
async def _like_profile(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Архив лайков анкеты пользовтеля"""
    if await state.get_state() == DisableProfile.waiting:
        return
    await state.set_state(LikeResponse.response)
    await update_user_username(callback.from_user.id, callback.from_user.username)
    await callback.message.answer(
        text=msg_text.SEARCH,
        reply_markup=arhive_search_kb
    )

    if liker_ids := await get_profile_likes(callback.from_user.id):
        await state.update_data(ids=liker_ids)
        profile = await get_profile(liker_ids[0])
        await send_profile(callback.from_user.id, profile)
    else:
        await callback.message.answer(msg_text.LIKE_ARCHIVE)
        await cancel_command(callback.message, state)


@router.message(LikeResponse.response, F.text.in_(["❤️", "👎"]))
async def _like_response(message: types.Message, state: FSMContext) -> None:
    """'Свайпы' людей которые лайкнули анкету пользователя"""
    data = await state.get_data()
    ids = data.get("ids")
    profile: Profile = await get_profile(ids[0])

    if message.text == "❤️":
        """Отправка пользователю которому ответили на лайк"""
        await sending_user_contact(
            user_id=profile.user_id.id,
            name=message.from_user.full_name,
            user_link=generate_user_link(
                user_id=message.from_user.id,
                username=message.from_user.username,
            )
        )

        """Отправка пользователю который ответил на лайк"""
        await sending_user_contact(
            user_id=message.from_user.id,
            name=profile.name,
            user_link=generate_user_link(
                user_id=profile.user_id.id,
                username=profile.user_id.username,
            )
        )

    await del_like(message.from_user.id, profile.user_id.id)

    ids.pop(0)
    await state.update_data(ids=ids)
    if ids:
        profile = await get_profile(ids[0])
        await send_profile(message.from_user.id, profile)
    else:
        await message.answer(msg_text.EMPTY_PROFILE_SEARCH)
        await cancel_command(message, state)
