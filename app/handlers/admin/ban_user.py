from aiogram import types
from aiogram.filters.state import StateFilter

from app.filters.kb_filter import BlockUserCallback
from app.handlers.message_text import admin_message_text as amt
from app.routers import admin_router as router
from database.services import Profile, User


@router.callback_query(BlockUserCallback.filter(), StateFilter(None))
async def _complaint_user_callback(callback: types.CallbackQuery, callback_data, session) -> None:
    """Блокирует пользователя переданого в калбек"""
    if user_id := callback_data.user_id:
        user = await User.get_with_profile(session, user_id)
        await User.update_isbanned(session, user, True)
        await Profile.update_isactive(session, user.profile, False)
        await callback.message.edit_text(amt.USER_BANNED.format(user.id))
    await callback.message.edit_text(amt.USER_BANNED_CANCEL)
