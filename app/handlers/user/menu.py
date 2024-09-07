from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, bot

from app.keyboards.default import  menu_kb
from app.handlers.msg_text import msg_text


@dp.message_handler(Command('menu'))
async def _menu(message: types.Message):
    await message.answer(msg_text.MENU, reply_markup=menu_kb())