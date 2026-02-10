from aiogram import types
from aiogram.filters import Command, CommandObject
from aiogram.filters.state import StateFilter
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.inline.admin import check_user_profile
from app.routers import admin_router
from app.services.profile_service import send_profile
from database.models import Profile


@admin_router.message(StateFilter(None), Command("profile"))
async def _profile_command(
    message: types.Message, command: CommandObject, session: AsyncSession
) -> None:
    """Админ панель"""
    profile_id = command.args.lower()
    profile = await Profile.get(session=session, id=int(profile_id))
    await send_profile(message.chat.id, profile, session)

    # Такая логика из за ограничений тг в том чтобы отправлять клавитары с webapp в группы
    if not message.chat.title:
        await message.answer(
            "Для действий с профилем",
            reply_markup=check_user_profile(profile.id),
        )
