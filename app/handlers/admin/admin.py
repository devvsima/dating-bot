from aiogram import types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from app.commands import set_admins_commands
from app.keyboards.default.base import admin_kb
from app.routers import admin_router


@admin_router.message(StateFilter(None), Command("admin"))
async def _admin_command(message: types.Message) -> None:
    """Админ панель"""
    await set_admins_commands(message.from_user.id)
    text = """
🔧 <b>Admin panel</b>

/admin - Admin panel
/ban - Block user
/unban - Unblock user
/stats - Send stats
/logs - Send logs
/mailing - Mailing to all users
/profile - Check user profile
/webapp - Webapp test
/restart - Update and restart bot
"""
    await message.answer(
        text=text,
        reply_markup=admin_kb,
        parse_mode="HTML",
    )
