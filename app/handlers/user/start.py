from aiogram import types, Dispatcher
from loader import dp, bot
from app.keyboards import start_kb, base_kb


@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    await message.answer(
        text="Выбери язык: ",
        reply_markup=start_kb(),
    )
    await message.delete()


@dp.message_handler(text=("🏳️Русский", "🇺🇦Українська", "🇬🇧English"))
async def start_command(message: types.Message):
    await message.answer(
        text="Привет, теперь давай создадим тебе профиль! Для создание нажми или напиши '/create'",
        reply_markup=base_kb(),
    )
    await message.delete()
