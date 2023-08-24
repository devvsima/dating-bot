from aiogram import types, Dispatcher
from loader import dp, bot
from app.handlers.user.create_profile import gender


@dp.message_handler(text="🔄")
async def retry_create_profile(message: types.Message):
    await gender(message)
