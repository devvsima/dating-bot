from aiogram import types
from aiogram.filters import Command, CommandObject
from aiogram.filters.state import StateFilter

from app.filters.kb_filter import BlockUserCallback
from app.handlers.bot_utils import check_args_type
from app.handlers.message_text import admin_message_text as amt
from app.routers import admin_router
from database.services import User


@admin_router.message(Command("ban"), StateFilter(None))
@admin_router.message(Command("unban"), StateFilter(None))
async def ban_unban_users_command(message: types.Message, command: CommandObject, session) -> None:
    """Блокирует или разблокирует пользователей, принимает список user_id через ','"""

    command_name = command.command.lower()
    is_banned = command_name == "ban"

    text_success = (
        "✅ Send user IDs separated by ',' to ban users.\nExample: <code>/ban 123456, 789012</code>"
        if is_banned
        else "✅ Send user IDs separated by ',' to unban users.\nExample: <code>/unban 123456, 789012</code>"
    )

    text_action = "🔒 Banned" if is_banned else "🔓 Unbanned"
    text_error = "⚠️ Error while updating status"

    if args := check_args_type(type=int, data_list=command.args):
        for user_id in args:
            try:
                await User.set_user_ban_and_profile_status(session, user_id, is_banned)
                await message.answer(f"✅ User <code>{user_id}</code> has been {text_action}.")
            except Exception:
                await message.answer(f"{text_error} for user <code>{user_id}</code>.")
    else:
        await message.answer(text_success)


@admin_router.callback_query(BlockUserCallback.filter(), StateFilter(None))
async def _complaint_user_callbackd(callback: types.CallbackQuery, callback_data, session) -> None:
    """Блокирует пользователя переданого в калбек"""
    if user_id := callback_data.user_id:
        await User.set_user_ban_and_profile_status(session, user_id, True)
        await callback.message.edit_text(amt.USER_BANNED.format(user_id))
    await callback.message.edit_text(amt.USER_BANNED_CANCEL)
