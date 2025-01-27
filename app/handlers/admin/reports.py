from aiogram import F, types

from app.routers import admin_router as router

from database.service.users import ban_or_unban_user

from app.handlers.msg_text import msg_text


@router.callback_query(F.data.startswith("block_user_"))
async def _block_user_callback(callback: types.CallbackQuery) -> None:
    """Блокирует пользователя переданого в калбек"""
    user_id = callback.data[11:]
    await ban_or_unban_user(int(user_id), True)
    await callback.message.edit_text(msg_text.USER_BANNED.format(user_id))
