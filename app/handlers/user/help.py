from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, bot

from data.config import IMAGES_DIR

from app.handlers.msg_text import msg_text


@dp.message_handler(Command('help'))
async def _help_command(message: types.Message):
    with open(f'{IMAGES_DIR}/logo.jpg', "rb") as photo:
        await message.answer_photo(photo=photo, caption=msg_text.INFO.format())
