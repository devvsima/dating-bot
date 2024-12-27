from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp

from app.handlers.msg_text import msg_text
from app.keyboards.default import  menu_kb


@dp.message_handler(Command('menu'))
async def menu(message: types.Message) -> None:
    await message.answer(msg_text.MENU, reply_markup=menu_kb())