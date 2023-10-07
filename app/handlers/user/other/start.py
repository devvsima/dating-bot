from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart

from loader import dp, bot, _
from app.keyboards import start_kb, base_selection, base_kb
from database.users import find_user


@dp.message_handler(CommandStart())
async def start_command(message: types.Message):
    user_language = message.from_user.id
    await message.answer(
        text=_("Выбери язык:"),
        reply_markup=start_kb(),
    )
    await message.delete()


@dp.message_handler(text=("Русский", "Українська", "English"))
async def lang_command(message: types.Message):
    db_us_id = await find_user(message.from_user.id)
    if db_us_id == None:
        await message.answer(
            text=_("Привет, теперь давай создадим тебе профиль! Для создание нажми или напиши '/create'"),
            reply_markup=base_kb(),
        )
    else:
        await message.answer(
            text=_("🔍 Искать анкеты \n👤 Мой профиль \n❌ Удалить профиль \n✉️ Пригласить друзей \n"),
            reply_markup=base_selection(),
        )
