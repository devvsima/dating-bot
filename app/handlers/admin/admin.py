from aiogram import types
from aiogram.dispatcher.filters import Command, Text

from loader import dp

from app.filters.admin import Admin
from app.handlers.msg_text import msg_text
from app.keyboards.inline.admin import admin_menu_ikb


@dp.message_handler(Admin(), Command("admin"))
async def _admin_command(message: types.Message) -> None:
    await message.answer(msg_text.ADMIN_WELCOME, reply_markup=admin_menu_ikb())

@dp.callback_query_handler(Text("admin"))
async def _admin_callback(callback: types.CallbackQuery) -> None:
    await callback.message.edit_text(msg_text.ADMIN_WELCOME, reply_markup=admin_menu_ikb())

