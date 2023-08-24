from aiogram import types, Dispatcher
from loader import dp, bot


@dp.message_handler(text="✉️")
async def invite_comm(message: types.Message):
    await message.answer("Ссылка для друзей:\nhttps://t.me/michalangelo_bot")
