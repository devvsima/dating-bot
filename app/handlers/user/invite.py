from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp, bot



@dp.message_handler(Text("✉️"))
async def _invitelink_command(message: types.Message):
    bot_user = await dp.bot.me
    await message.answer(
        f"Приглашай друзей и получай бонус к своей анкете!\n\nСсылка для друзей:\n<code>https://t.me/{bot_user.username}?start={message.from_user.id}</code>"
        )
