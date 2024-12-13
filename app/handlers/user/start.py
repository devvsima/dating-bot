from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from loader import dp
from data.config import DIR

from database.service.profile import get_profile

from app.handlers.msg_text import msg_text
from app.keyboards.default import  start_kb
from .menu import _menu
from database.service.users import new_referral, get_or_create_user

@dp.message_handler(CommandStart())
async def _start_command(message: types.Message, user):
    if await get_profile(message.from_user.id):
        await _menu(message)
    else:
        with open(f'{DIR}/photo/logo.jpg', "rb") as photo:
            await message.answer_photo(
                photo=photo,
                caption=(msg_text.WELCOME),
                reply_markup=start_kb(),
            )
