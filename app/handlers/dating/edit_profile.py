from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

import app.filters.create_profile_filtres as filters
from app.handlers.dating.profile import profile_command
from app.routers import dating_router
from app.states.default import ProfileEdit
from app.text import message_text as mt
from database.models import UserModel
from database.services import Profile


@dating_router.message(StateFilter(None), F.text == "🖼")
async def _edit_profile_photo_command(message: types.Message, state: FSMContext) -> None:
    """Редактирует фотографию пользователя"""
    await state.set_state(ProfileEdit.photo)
    await message.answer(mt.PHOTO)


@dating_router.message(StateFilter(ProfileEdit.photo), filters.IsPhoto())
async def _update_photo(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """Обновляет фотографию профиля"""
    await Profile.update(
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
    await message.answer(mt.DESCRIPTION)


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
