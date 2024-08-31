from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from loader import dp, bot

from database.service.profile import is_profile
from database.service.users import new_referral

from app.handlers import msg_text
from app.keyboards.default import  base_kb
from .menu import _menu


@dp.message_handler(CommandStart())
async def _start_command(message: types.Message):
    if await is_profile(message.from_user.id):
        await _menu(message)
    else:
        args = message.get_args()
        # if args:
        #     new_referral(message.from_user.id, args)
        from data.config import DIR
        with open(f'{DIR}/photo/logo.jpg', "rb") as photo:
        
            await message.answer_photo(
                photo=photo,
                caption=(msg_text.WELCOME),
                reply_markup=base_kb(),
            )
