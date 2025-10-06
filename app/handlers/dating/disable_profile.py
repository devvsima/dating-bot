from aiogram import F, types
from aiogram.filters.state import StateFilter
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.default.base import start_kb
from app.routers import dating_router
from app.text import message_text as mt
from database.models import UserModel
from database.services import Profile


@dating_router.message(StateFilter(None), F.text == "❌")
async def _disable_profile_command(
    message: types.Message, user: UserModel, session: AsyncSession
) -> None:
    """Отключает профиль пользователя, и не дает ему дальше пользоватся ботом до восстановления"""
    await Profile.update(
        session=session,
        id=user.id,
        is_active=False,
    )
    await message.answer(text=mt.DISABLE_PROFILE, reply_markup=start_kb)
