from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart

from loader import dp, bot
from app.keyboards.default import  base_kb, menu_kb
from database.service.users import find_user


@dp.message_handler(CommandStart())
async def _start_command(message: types.Message):
    db_us_id = await find_user(message.from_user.id)
    if not db_us_id:
        await message.answer(
            text=("Привет, теперь давай создадим тебе профиль! Для создание нажми или напиши '/create'"),
            reply_markup=base_kb(),
        )
    else:
        await message.answer(
            text=("🔍 Искать анкеты \n👤 Мой профиль \n✉️ Пригласить друзей \n"),
            reply_markup=menu_kb(),
        )
