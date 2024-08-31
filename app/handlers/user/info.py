from aiogram import types
from aiogram.dispatcher.filters import Command, Text

from loader import dp, bot

from data.config import DIR

from app.keyboards.default import  base_kb
from .menu import _menu

from app.handlers import msg_text
@dp.message_handler(Command('info'))
async def _start_command(message: types.Message):

    with open(f'{DIR}/photo/logo.jpg', "rb") as photo:
        await message.answer_photo(photo=photo, caption=msg_text.INFO.format())
