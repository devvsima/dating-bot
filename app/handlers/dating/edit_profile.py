from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from app.handlers.message_text import user_message_text as umt
from app.others.states import ProfileEdit
from app.routers import dating_router
from database.models import UserModel
from database.services import Profile


@dating_router.message(F.text == "🖼", StateFilter(None))
async def _edit_profile_photo_command(message: types.Message, state: FSMContext) -> None:
    """Редактирует фотографию пользователя"""
    await state.set_state(ProfileEdit.photo)
    await message.answer(umt.PHOTO)


@dating_router.message(F.text == "✍️", StateFilter(None))
async def _edit_profile_description_command(message: types.Message, state: FSMContext) -> None:
    """Редактирует описание пользователя"""
    await state.set_state(ProfileEdit.desc)
    await message.answer(umt.DESCRIPTION)


@dating_router.message(F.text == "❌", StateFilter(None))
async def _disable_profile_command(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """Отключает профиль пользователя, и не дает ему дальше пользоватся ботом до восстановления"""
    await Profile.update_isactive(session, user.profile, False)
    await message.answer(text=umt.DISABLE_PROFILE)
