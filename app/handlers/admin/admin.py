from aiogram import types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from app.handlers.msg_text import msg_text
from app.keyboards.default.admin import admin_menu_kb
from app.routers import admin_router as router


@router.message(Command("admin"), StateFilter(None))
async def _admin_command(message: types.Message) -> None:
    """Админ панель"""
    await message.answer(text=msg_text.ADMIN_WELCOME, reply_markup=admin_menu_kb())
