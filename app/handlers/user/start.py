from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from loader import dp
from data.config import DIR

from database.service.profile import is_profile

from app.handlers.msg_text import msg_text
from app.keyboards.default import  start_kb
from .menu import _menu


@dp.message_handler(CommandStart())
async def _start_command(message: types.Message):
    if await is_profile(message.from_user.id):
        await _menu(message)
    else:
        args = message.get_args()
        with open(f'{DIR}/photo/logo.jpg', "rb") as photo:
            await message.answer_photo(
                photo=photo,
                caption=(msg_text.WELCOME),
                reply_markup=start_kb(),
            )
