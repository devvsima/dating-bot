from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, bot

from data.config import DIR

from app.handlers.msg_text import msg_text


@dp.message_handler(Command('info'))
async def _info_command(message: types.Message):
    with open(f'{DIR}/photo/logo.jpg', "rb") as photo:
        await message.answer_photo(photo=photo, caption=msg_text.INFO.format())
