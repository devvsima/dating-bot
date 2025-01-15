from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp

from app.filters.admin import IsAdmin
from app.keyboards.default.admin import admin_menu_kb

from app.handlers.msg_text import msg_text


@dp.message_handler(IsAdmin(), Command("admin"))
async def _admin_command(message: types.Message) -> None:
    """Админ панель"""
    await message.answer(msg_text.ADMIN_WELCOME, reply_markup=admin_menu_kb())
