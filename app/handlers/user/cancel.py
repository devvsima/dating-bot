from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp, bot
from app.keyboards import *


# выключение машины состояний
@dp.message_handler(Command("cancel"), state="*")
async def _cancel_command(message: types.message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.answer(("Вы вышли с создания анкеты."))

    await message.answer(
        """
        \t🔍Смотреть анкеты
👤Моя анкета
❌Удалить анкету
✉️Пригласить друзей
        """,
        reply_markup=base_selection(),
    )
