from aiogram import F, types
from aiogram.fsm.context import FSMContext

from app.routers import user_router as router

from database.service.profile import delete_profile

from app.handlers.msg_text import msg_text
from app.keyboards.inline.profile import delete_profile_ikb
from app.others.states import ProfileEdit
from .profile import profile_command


@router.message(F.text == "🖼")
async def _edit_profile_photo_command(
    message: types.Message, state: FSMContext
) -> None:
    """Редактирование фотографии"""
    await state.set_state(ProfileEdit.photo)
    await message.answer(msg_text.PHOTO)


@router.message(F.text == "✍️")
async def _edit_profile_description_command(
    message: types.Message, state: FSMContext
) -> None:
    """Редактирование описания"""
    await state.set_state(ProfileEdit.desc)
    await message.answer(msg_text.DESCRIPTION)


@router.message(F.text == "❌")
async def _delete_profile_command(message: types.Message, state: FSMContext) -> None:
    """1/2 Удаление профиля"""
    await message.answer(msg_text.DELETE_PROFILE, reply_markup=delete_profile_ikb())


@router.callback_query(F.data.in_(["delete_yes", "delete_no"]))
async def _delete_profile_choice(callback: types.CallbackQuery) -> None:
    """2/2 Удаление профиля"""
    if callback.data == "delete_yes":
        await delete_profile(callback.from_user.id)
        await callback.message.answer(msg_text.DELETE_PROFILE_ALERT)
    elif callback.data == "delete_no":
        await profile_command()
