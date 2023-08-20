from aiogram import types, Dispatcher
from loader import dp, bot
from app.keyboards import *


@dp.message_handler(text="ㅤ👤ㅤ")
async def profile_comm(message: types.Message):
    # await message.answer
    await message.answer(
        """
        🔄 Заполнить профиль заново
🖼 Сменить фото
✍️ Сменить описание
🔍 Смотреть анкеты
        """,
        reply_markup=comm_profile(),
    )
