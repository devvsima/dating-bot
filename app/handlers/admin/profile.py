from aiogram import types
from aiogram.filters import Command, CommandObject
from aiogram.filters.state import StateFilter
from sqlalchemy.ext.asyncio import AsyncSession

from app.business.profile_service import send_profile
from app.routers import admin_router
from database.services.profile import Profile


@admin_router.message(StateFilter(None), Command("profile"))
async def _admin_command(
    message: types.Message, command: CommandObject, session: AsyncSession
) -> None:
    """Админ панель"""
    try:
        profile_id = command.args.lower()
        profile = await Profile.get(session=session, id=int(profile_id))
        await send_profile(message.chat.id, profile, session)
    except:
        await message.answer("Profile not found")
