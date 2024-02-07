from aiogram import types
from loader import dp, bot
from app.handlers.user.other.create_profile import gender


@dp.message_handler(text="🔄")
async def retry_create_profile(message: types.Message):
    await gender(message)
