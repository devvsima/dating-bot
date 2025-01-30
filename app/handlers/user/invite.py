from aiogram import F, types
from aiogram.filters.state import StateFilter

from loader import bot

from app.routers import user_router as router

from database.models.users import Users

from app.handlers.msg_text import msg_text

from utils.base62 import encode_base62


@router.message(F.text == "✉️", StateFilter(None))
async def _invite_link_command(message: types.Message, user: Users) -> None:
    """Дает пользователю его реферальную ссылку"""
    bot_user = await bot.get_me()
    user_code: str = encode_base62(message.from_user.id)
    await message.answer(msg_text.INVITE_FRIENDS.format(
        user.referral, bot_user.username, user_code
        )
    )
