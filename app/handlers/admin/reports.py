from aiogram import F, types
from aiogram.filters.state import StateFilter

from app.handlers.msg_text import msg_text
from app.routers import admin_router as router
from database.services import User


@router.callback_query(F.data.startswith("block_user_"), StateFilter(None))
async def _block_user_callback(callback: types.CallbackQuery, session) -> None:
    """Блокирует пользователя переданого в калбек"""
    user_id = int(callback.data[11:])
    await User.update_isbanned(session, user_id, True)
    await callback.message.edit_text(msg_text.USER_BANNED.format(user_id))
