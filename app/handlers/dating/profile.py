from aiogram import F, types
from aiogram.filters.state import StateFilter
from sqlalchemy.ext.asyncio import AsyncSession

from app.business.menu_service import menu
from app.business.profile_service import send_profile
from app.keyboards.default.base import profile_kb
from app.routers import dating_router
from app.text import message_text as mt
from database.models import UserModel


@dating_router.message(StateFilter(None), F.text == "👤")
async def profile_command(message: types.Message, user: UserModel, session: AsyncSession) -> None:
    """Отправляет профиль пользователя"""

    # Проверяем, есть ли у пользователя профиль
    if not user.profile:
        await message.answer(mt.NO_PROFILE_FOR_SEARCH)
        await menu(message.from_user.id)
        return

    await send_profile(message.from_user.id, user.profile, session)
    await message.answer(mt.PROFILE_MENU, reply_markup=profile_kb)


@dating_router.message(StateFilter(None), F.text == "↩️")
async def _return_to_menu(message: types.Message) -> None:
    await menu(message.from_user.id)
