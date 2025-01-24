from aiogram import types
from aiogram.filters import Command

from app.routers import admin_router as router

from app.filters.admin import IsAdmin
from app.keyboards.default.admin import admin_menu_kb

from app.handlers.msg_text import msg_text


@router.message(IsAdmin(), Command("admin"))
async def _admin_command(message: types.Message) -> None:
    """Админ панель"""
    await message.answer(msg_text.ADMIN_WELCOME, reply_markup=admin_menu_kb())
