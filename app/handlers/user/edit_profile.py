from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from database.service.profile import update_profile_is_active_status

from app.routers import user_router as router

from app.handlers.msg_text import msg_text
from app.handlers.bot_utils import menu
from app.others.states import ProfileEdit, DisableProfile
from app.keyboards.default.base import profile_return_kb


@router.message(F.text == "🖼", StateFilter(None))
async def _edit_profile_photo_command(message: types.Message, state: FSMContext) -> None:
    """Редактирование фотографии"""
    await state.set_state(ProfileEdit.photo)
    await message.answer(msg_text.PHOTO)


@router.message(F.text == "✍️", StateFilter(None))
async def _edit_profile_description_command(message: types.Message, state: FSMContext) -> None:
    """Редактирование описания"""
    await state.set_state(ProfileEdit.desc)
    await message.answer(msg_text.DESCRIPTION)
    
@router.message(F.text == "❌", StateFilter(None))
async def _disable_profile_command(message: types.Message, state: FSMContext) -> None:
    """Отключение профиля"""
    await state.set_state(DisableProfile.waiting)
    await update_profile_is_active_status(message.from_user.id, False)
    await message.answer(
        text = msg_text.DISABLE_PROFILE,
        reply_markup = profile_return_kb()
    )
    

@router.message(F.text.in_(
["🔙 Вернуть профиль", "🔙 Return profile", "🔙 Повернути профіль"]
    ), DisableProfile.waiting)
async def _activate_profile_command(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await update_profile_is_active_status(message.from_user.id, True)
    await message.answer(msg_text.ACTIVATE_PROFILE_ALERT)
    await menu(message.from_user.id)
    