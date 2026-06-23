from aiogram import types
from aiogram.filters import Command, CommandObject
from aiogram.filters.state import StateFilter
from sqlalchemy.ext.asyncio import AsyncSession

from app.routers import admin_router
from app.services.profile_service import send_profile
from database.models import Profile


@admin_router.message(StateFilter(None), Command("profile"))
async def _profile_command(
    message: types.Message, command: CommandObject, session: AsyncSession
) -> None:
    """Админ панель"""
    profile_id = command.args.lower()
    profile = await Profile.get_by_id(session=session, id=int(profile_id))
    if profile:
        await send_profile(
            chat_id=message.chat.id,
            profile=profile,
            session=session,
        )
        return
    await message.answer("Profile not found")
