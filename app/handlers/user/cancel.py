from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp, bot
from app.keyboards.default import menu_kb


# выключение машины состояний
@dp.message_handler(Command("cancel"), state="*")
async def _cancel_command(message: types.message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.answer("Вы вышли из сосздания анкеты.")
    
    text=("🔍 Искать анкеты \n👤 Мой профиль \n\n✉️ Пригласить друзей \n"),
    await message.answer(text,
        reply_markup=menu_kb(),
    )
