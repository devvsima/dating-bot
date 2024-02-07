from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp, bot


@dp.message_handler(Text("✉️"))
async def invite_comm(message: types.Message):
    bot_user = await dp.bot.me
    await message.answer(f"Ссылка для друзей:\nhttps://t.me/{bot_user.username}?start={message.from_user.id}")
