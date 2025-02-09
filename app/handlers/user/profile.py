from aiogram import F, types
from aiogram.filters.state import StateFilter

from app.handlers.bot_utils import send_profile
from app.handlers.msg_text import msg_text
from app.keyboards.default.base import profile_kb
from app.routers import user_router as router
from database.models import UserModel


@router.message(F.text == "👤", StateFilter(None))
async def profile_command(message: types.Message, user: UserModel) -> None:
    """Отправляет профиль пользователя"""
    await send_profile(message.from_user.id, user.profile)
    await message.answer(msg_text.PROFILE_MENU, reply_markup=profile_kb)
