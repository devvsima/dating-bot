from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from loader import dp
from data.config import IMAGES_DIR

from database.service.profile import get_profile

from app.handlers.msg_text import msg_text
from app.keyboards.default import  start_kb
from app.handlers.bot_utils import menu


@dp.message_handler(CommandStart())
async def _start_command(message: types.Message) -> None:
    """Стратовая команда"""
    if await get_profile(message.from_user.id):
        await menu(message.from_user.id)
    else:
        with open(f'{IMAGES_DIR}/christmas_logo.png', "rb") as photo:
            await message.answer_photo(
                photo=photo,
                caption=msg_text.WELCOME,
                reply_markup=start_kb(),
            )