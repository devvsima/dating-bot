from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from loader import dp

from app.handlers.bot_utils import menu

@dp.message_handler(Text("💤"), state="*")
@dp.message_handler(Command("cancel"), state="*")
async def cancel_command(message: types.Message, state: FSMContext) -> None:
    if state is None:
        return
    await state.finish()
    await menu(message.from_user.id)