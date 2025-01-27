from aiogram import F, types

from loader import bot

from app.routers import user_router as router

from database.models.users import Users

from app.handlers.msg_text import msg_text


@router.message(F.text == "✉️")
async def _invite_link_command(message: types.Message, user: Users) -> None:
    """Дает пользователю его реферальную ссылку"""
    bot_user = await bot.get_me()
    await message.answer(msg_text.INVITE_FRIENDS.format(
        user.referral,
        bot_user.username,
        message.from_user.id
        )
    )
