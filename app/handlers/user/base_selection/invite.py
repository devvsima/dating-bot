from aiogram import types, Dispatcher
from loader import dp, bot,_


@dp.message_handler(text="✉️")
async def invite_comm(message: types.Message):
    bot_user = await dp.bot.me
    await message.answer(f"Ссылка для друзей:\nhttps://t.me/{bot_user.username}?start={message.from_user.id}")
