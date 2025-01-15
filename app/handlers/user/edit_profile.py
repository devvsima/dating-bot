from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp

from database.service.profile import delete_profile

from app.handlers.msg_text import msg_text
from app.keyboards.inline.profile import delete_profile_ikb
from app.states.profile_create_state import ProfileEdit
from .profile import profile_command


@dp.message_handler(Text("🖼"))
async def _edit_profile_photo_command(message: types.Message) -> None:
    """Редактирование фотографии"""
    await ProfileEdit.photo.set()
    await message.answer(msg_text.PHOTO)

@dp.message_handler(Text("✍️"))
async def _edit_profile_description_command(message: types.Message) -> None:
    """Редактирование описания"""
    await ProfileEdit.desc.set()
    await message.answer(msg_text.DESCRIPTION)

@dp.message_handler(Text("❌"))
async def _delete_profile_command(message: types.Message) -> None:
    """1/2 Удаление профиля"""
    await message.answer(msg_text.DELETE_PROFILE, reply_markup=delete_profile_ikb())

@dp.callback_query_handler(Text(["delete_yes", "delete_no"]))
async def _delete_profile_choice(callback: types.CallbackQuery) -> None:
    """2/2 Удаление профиля"""
    if callback.data == "delete_yes":
        await delete_profile(callback.from_user.id)
        await callback.message.answer(msg_text.DELETE_PROFILE_ALERT)
    elif callback.data == "delete_no":
        await profile_command()

