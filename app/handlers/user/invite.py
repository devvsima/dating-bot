from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp

from database.models.users import Users

from app.handlers.msg_text import msg_text


@dp.message_handler(Text("✉️"))
async def _invite_link_command(message: types.Message, user: Users) -> None:
    """Дает пользователю его реферальную ссылку"""
    bot_user = await dp.bot.me
    await message.answer(msg_text.INVITE_FRIENDS.format(user.referral, bot_user.username, message.from_user.id))
