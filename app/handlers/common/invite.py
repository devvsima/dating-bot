from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.utils.deep_linking import create_start_link
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.default.base import return_to_menu_kb
from app.routers import common_router
from app.text import message_text as mt
from core.loader import bot
from database.models import Referal, UserModel
from utils.base62 import encode_base62


@common_router.message(StateFilter(None), F.text == "✉️")
async def _invite_link_command(
    message: types.Message, user: UserModel, session: AsyncSession
) -> None:
    """Отправляет персональную реферальную ссылку для приглашения друзей.
    Ссылка создается на основе пользовательского id и кодировки base62"""
    user_code: str = encode_base62(message.from_user.id)
    url = await create_start_link(bot, f"usr_{user_code}")
    invites_count = await Referal.get_invites_count(session, user.id)

    text = mt.INVITE_FRIENDS.format(invites_count, url)
    await message.answer(
        text=text,
        reply_markup=return_to_menu_kb,
        # Нужно реализовать отправку приглашений через контакты
        # reply_markup=referal_ikb(url=url),
    )
