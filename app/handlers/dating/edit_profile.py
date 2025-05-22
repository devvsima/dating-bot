from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

import app.filters.create_profile_filtres as filters
from app.handlers.dating.profile import profile_command
from app.handlers.message_text import user_message_text as umt
from app.others.states import ProfileEdit
from app.routers import dating_router
from database.models import UserModel
from database.services import Profile


@dating_router.message(StateFilter(None), F.text == "🖼")
async def _edit_profile_photo_command(message: types.Message, state: FSMContext) -> None:
    """Редактирует фотографию пользователя"""
    await state.set_state(ProfileEdit.photo)
    await message.answer(umt.PHOTO)


@dating_router.message(StateFilter(ProfileEdit.photo), filters.IsPhoto())
async def _update_photo(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """Обновляет фотографию профиля"""
    await Profile.update_photo(
        session=session,
        id=user.id,
        photo=message.photo[0].file_id,
    )
    await state.clear()
    await profile_command(message, user)


@dating_router.message(StateFilter(None), F.text == "✍️")
async def _edit_profile_description_command(message: types.Message, state: FSMContext) -> None:
    """Редактирует описание пользователя"""
    await state.set_state(ProfileEdit.description)
    await message.answer(umt.DESCRIPTION)


@dating_router.message(StateFilter(ProfileEdit.description))
async def _update_photo(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """Обновляет описание профиля"""
    await Profile.update(
        session=session,
        id=user.id,
        description=message.text,
    )
    await state.clear()
    await profile_command(message, user)


@dating_router.message(StateFilter(None), F.text == "❌")
async def _disable_profile_command(message: types.Message, user: UserModel, session) -> None:
    """Отключает профиль пользователя, и не дает ему дальше пользоватся ботом до восстановления"""
    await Profile.update(
        session=session,
        id=user.id,
        is_active=False,
    )
    await message.answer(text=umt.DISABLE_PROFILE)
