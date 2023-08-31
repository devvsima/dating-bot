from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart

from loader import dp, bot
from app.keyboards import start_kb, base_selection, base_kb
from database.bd import get_user_id


@dp.message_handler(CommandStart())
async def start_command(message: types.Message):
    user_language = message.from_user.id
    await message.answer(
        text="Выбери язык: ",
        reply_markup=start_kb(),
    )
    await message.delete()


@dp.message_handler(text=("Русский", "Українська", "English"))
async def lang_command(message: types.Message):
    db_us_id = get_user_id(str(message.from_user.id))
    print(str(message.from_user.id))
    print(str(db_us_id))
    # print(str(db_us_id[0]))
    if db_us_id == None:
        await message.answer(
            text="Привет, теперь давай создадим тебе профиль! Для создание нажми или напиши '/create'",
            reply_markup=base_kb(),
        )
    elif str(message.from_user.id) == db_us_id[0]:
        await message.answer(
            text="🔍 Искать анкеты \n👤 Мой профиль \n❌ Удалить профиль \n✉️ Пригласить друзей \n",
            reply_markup=base_selection(),
        )
