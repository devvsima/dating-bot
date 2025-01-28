from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from app.routers import user_router as router

from app.handlers.msg_text import msg_text
from app.others.states import ProfileEdit


@router.message(F.text == "🖼", StateFilter(None))
async def _edit_profile_photo_command(
    message: types.Message, state: FSMContext
) -> None:
    """Редактирование фотографии"""
    await state.set_state(ProfileEdit.photo)
    await message.answer(msg_text.PHOTO)


@router.message(F.text == "✍️", StateFilter(None))
async def _edit_profile_description_command(
    message: types.Message, state: FSMContext
) -> None:
    """Редактирование описания"""
    await state.set_state(ProfileEdit.desc)
    await message.answer(msg_text.DESCRIPTION)
    
