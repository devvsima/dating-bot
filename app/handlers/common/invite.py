from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.utils.deep_linking import create_start_link

from app.routers import common_router
from app.text import message_text as mt
from database.models import UserModel
from database.services.referal import Referal
from loader import bot
from utils.base62 import encode_base62


@common_router.message(StateFilter(None), F.text == "✉️")
async def _invite_link_command(message: types.Message, user: UserModel, session) -> None:
    """Отправляет персональную реферальную ссылку для приглашения друзей.
    Ссылка создается на основе пользовательского id и кодировки base62"""
    user_code: str = encode_base62(message.from_user.id)
    url = await create_start_link(bot, f"usr_{user_code}")
    invites_count = await Referal.get_invites_count(session, user.id)

    await message.answer(mt.INVITE_FRIENDS.format(invites_count, url))
