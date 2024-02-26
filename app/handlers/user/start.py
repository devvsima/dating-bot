from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart

from loader import dp, bot
from app.keyboards.default import  base_kb, menu_kb
from database.service.profile import if_profile


@dp.message_handler(CommandStart())
async def _start_command(message: types.Message):
    db_us_id = await if_profile(message.from_user.id)
    print(db_us_id)
    if db_us_id:
        await message.answer(
            text=("🔍 Искать анкеты \n👤 Мой профиль \n✉️ Пригласить друзей \n"),
            reply_markup=menu_kb(),

        )
    else:
        await message.answer(
            text=("Привет, теперь давай создадим тебе профиль! Для создание нажми или напиши '/create'"),
            reply_markup=base_kb(),
        )
