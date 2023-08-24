from aiogram import types, Dispatcher
from loader import dp, bot
from app.keyboards import start_kb, base_selection, base_kb
from aiogram.utils.callback_data import CallbackData
from database.bd import get_user_id


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
    print(str(message.from_user.id))
    print(get_user_id(message.from_user.id))
    if str(message.from_user.id) == get_user_id(message.from_user.id)[0]:
        await message.answer(
            text="🔍 Искать анкеты \n👤 Мой профиль \n❌ Удалить профиль \n✉️ Пригласить друзей \n",
            reply_markup=base_selection(),
        )
    else:
        await message.answer(
            text="Привет, теперь давай создадим тебе профиль! Для создание нажми или напиши '/create'",
            reply_markup=base_kb(),
        )

    mess = message.from_user
    await message.delete()
