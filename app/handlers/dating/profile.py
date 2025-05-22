from aiogram import F, types
from aiogram.filters.state import StateFilter

from app.handlers.bot_utils import menu, send_profile
from app.handlers.message_text import user_message_text as umt
from app.keyboards.default.base import profile_kb
from app.routers import dating_router
from database.models import UserModel


@dating_router.message(StateFilter(None), F.text == "👤")
async def profile_command(message: types.Message, user: UserModel) -> None:
    """Отправляет профиль пользователя"""
    await send_profile(message.from_user.id, user.profile)
    await message.answer(umt.PROFILE_MENU, reply_markup=profile_kb)


@dating_router.message(StateFilter(None), F.text == "↩️")
async def _return_to_menu(message: types.Message) -> None:
    await menu(message.from_user.id)
