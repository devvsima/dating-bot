from aiogram import F, types

from app.routers import user_router as router

from database.service.profile import get_profile

from app.handlers.msg_text import msg_text
from app.handlers.bot_utils import send_profile
from app.keyboards.default import profile_kb


@router.message(F.text == "👤")
async def profile_command(message: types.Message) -> None:
    """Отправляет профиль пользователя"""
    profile = await get_profile(message.from_user.id)

    await send_profile(message.from_user.id, profile)
    await message.answer(msg_text.PROFILE_MENU, reply_markup=profile_kb())
