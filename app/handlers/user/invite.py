from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp, bot

from app.handlers import msg_text


@dp.message_handler(Text("✉️"))
async def _invitelink_command(message: types.Message):
    bot_user = await dp.bot.me
    await message.answer(msg_text.INVITE_FRIENDS.format(bot_user.username, bot_user.username))
