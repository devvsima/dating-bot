from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, bot

from database.service.profile import is_profile

from app.keyboards.default import  menu_kb


@dp.message_handler(Command('menu'))
async def _menu(message: types.Message):
    if await is_profile(message.from_user.id):
        await message.answer(
            text=("🔍 Искать анкеты \n👤 Мой профиль \n\n✉️ Пригласить друзей \n"),
            reply_markup=menu_kb(),

        )