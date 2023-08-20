from aiogram import types, Dispatcher
from loader import dp, bot
from app.keyboards import start_kb, base_selection
from aiogram.utils.callback_data import CallbackData


@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    user_language = message.from_user.id
    await message.answer(
        text="Выбери язык: ",
        reply_markup=start_kb(),
    )
    await message.delete()


@dp.message_handler(text=("🏳️Русский", "🇺🇦Українська", "🇬🇧English"))
async def lang_command(message: types.Message):
    await message.answer(
        text="Привет, теперь давай создадим тебе профиль! Для создание нажми или напиши '/create'",
        reply_markup=base_selection(),
    )
    # user_id = message.from_user.id
    mess = message.from_user
    # print(mess)
    await message.delete()
