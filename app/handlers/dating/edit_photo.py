from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

import app.filters.create_profile_filtres as filters
from app.handlers.dating.profile import profile_command
from app.keyboards.default.registration_form import RegistrationFormKb
from app.routers import dating_router
from app.states.default import ProfileEdit
from app.text import message_text as mt
from database.models import UserModel
from database.services import Profile


@dating_router.message(StateFilter(None), F.text == "🖼")
async def _edit_profile_photo_command(
    message: types.Message, state: FSMContext, user: UserModel
) -> None:
    """Редактирует фотографию пользователя"""
    await state.set_state(ProfileEdit.photo)

    kb = RegistrationFormKb.photo(user)
    await message.answer(
        text=mt.PHOTO,
        reply_markup=kb,
    )


@dating_router.message(StateFilter(ProfileEdit.photo), filters.IsPhoto())
async def _update_photo(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """Обновляет фотографию профиля"""
    photo = (
        user.profile.photo
        if message.text in filters.leave_previous_tuple
        else message.photo[0].file_id
    )
    await Profile.update(session=session, id=user.id, photo=photo)
    await state.clear()
    await profile_command(message, user)
