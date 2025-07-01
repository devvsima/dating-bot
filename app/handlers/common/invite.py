from aiogram import F, types
from aiogram.filters.state import StateFilter

from app.routers import common_router
from app.text import message_text as mt
from database.models import UserModel
from loader import bot
from utils.base62 import encode_base62


@common_router.message(StateFilter(None), F.text == "✉️")
async def _invite_link_command(message: types.Message, user: UserModel) -> None:
    """Отправляет персональную реферальную ссылку для приглашения друзей.
    Ссылка создается на основе пользовательского id и кодировки base62"""
    bot_user = await bot.get_me()
    user_code: str = encode_base62(message.from_user.id)
    await message.answer(mt.INVITE_FRIENDS.format(user.referral, bot_user.username, user_code))
