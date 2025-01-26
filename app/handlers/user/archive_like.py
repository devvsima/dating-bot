from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from loader import bot
from app.routers import user_router as router

from database.service.likes import get_profile_likes, del_like
from database.service.profile import get_profile

from .profile import send_profile
from .cancel import cancel_command
from app.handlers.msg_text import msg_text
from app.others.states import LikeResponse
from app.keyboards.default import search_kb


@router.message(F.text == "🗄", StateFilter("*"))
async def like_profile(message: types.Message, state: FSMContext) -> None:
    """Архив лайков анкеты пользовтеля"""
    await message.answer(text=msg_text.SEARCH, reply_markup=search_kb())
    await state.set_state(LikeResponse.response)

    liker_ids = get_profile_likes(message.from_user.id)

    if not liker_ids:
        await message.answer(msg_text.LIKE_ARCHIVE)
        await cancel_command(message, state)
        return
    else:
        await state.update_data(ids=liker_ids)
        profile = await get_profile(liker_ids[0])
        await send_profile(message.from_user.id, profile)


@router.callback_query(F.data == "archive", StateFilter("*"))
async def _like_profile(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(text=msg_text.SEARCH, reply_markup=search_kb())
    await state.set_state(LikeResponse.response)

    liker_ids = get_profile_likes(int(callback.from_user.id))
    if not liker_ids:
        await callback.message.answer(msg_text.LIKE_ARCHIVE)
        await cancel_command(callback.message, state)
        return
    else:
        await state.update_data(ids=liker_ids)
        profile = await get_profile(liker_ids[0])
        await send_profile(callback.from_user.id, profile)


username_url = "https://t.me/{}"
id_url = "tg://user?id={}"


@router.message(F.text.in_(["❤️", "👎"]), StateFilter(LikeResponse.response))
async def _like_response(message: types.Message, state: FSMContext) -> None:
    """'Свайпы' людей которые лайкнули анкету пользователя"""
    data = await state.get_data()
    ids = data.get("ids")
    profile = await get_profile(ids[0])

    if message.text == "❤️":
        """Отправка пользователю которому ответили на лайк"""
        url = id_url.format(message.from_user.id)
        if message.from_user.username:
            url = username_url.format(message.from_user.username)

        await bot.send_message(
            chat_id=profile.user_id.id,
            text=msg_text.LIKE_ACCEPT.format(url, message.from_user.full_name),
        )

        """Отправка пользователю который ответил на лайк"""
        url = id_url.format(profile.user_id.id)
        if profile.user_id.username:
            url = username_url.format(profile.user_id.username)

        await bot.send_message(
            chat_id=message.from_user.id,
            text=msg_text.LIKE_ACCEPT.format(url, profile.name),
        )

    elif message.text == "👎":
        pass
    del_like(message.from_user.id, profile.user_id.id)

    ids.pop(0)
    await state.update_data(ids=ids)
    if not ids:
        await message.answer(msg_text.EMPTY_PROFILE_SEARCH)
        await cancel_command(message, state)
        return
    else:
        profile = await get_profile(ids[0])
        await send_profile(message.from_user.id, profile)
