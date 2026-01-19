import re

from aiogram import types
from aiogram.filters import Command, CommandObject
from aiogram.filters.state import StateFilter
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.kb_filter import BlockUserCallback
from app.routers import admin_router
from database.models.complaint import ComplaintStatus
from database.services.complaint import Complaint
from database.services.user import User


@admin_router.message(StateFilter(None), Command("ban"))
@admin_router.message(StateFilter(None), Command("unban"))
async def ban_unban_users_command(
    message: types.Message, command: CommandObject, session: AsyncSession
) -> None:
    """Блокирует или разблокирует пользователей, принимает список id через ','"""

    command_name = command.command.lower()
    is_banned = command_name == "ban"
    text_success, text_action, text_error = get_ban_text(is_banned)

    if args := check_args_type(type=int, data_list=command.args):
        for id in args:
            try:
                if is_banned:
                    await User.ban(session, id)
                else:
                    await User.unban(session, id)
                await message.answer(f"✅ User <code>{id}</code> has been {text_action}.")
            except Exception:
                await message.answer(f"{text_error} for user <code>{id}</code>.")
    else:
        await message.answer(text_success)


@admin_router.callback_query(StateFilter(None), BlockUserCallback.filter())
async def _complaint_user_callback(
    callback: types.CallbackQuery, callback_data: BlockUserCallback, session: AsyncSession
) -> None:
    """Блокирует пользователя переданого в калбек"""
    complaint_id = callback_data.complaint_id
    receiver_id = callback_data.receiver_id
    receiver_username = callback_data.receiver_username

    # Получаем информацию о жалобе, включая отправителя
    complaint = await Complaint.get_by_id(session=session, id=complaint_id)
    sender_user = (
        await User.get_by_id(session=session, id=complaint.sender_id) if complaint else None
    )

    if callback_data.ban:
        await User.ban(session=session, id=receiver_id)
        await Complaint.update(session=session, id=complaint_id, status=ComplaintStatus.Accepted)
        text = "⛔️ Administrator <code>{admin_id}</code> @{admin_username} \
accepted a request to block user <code>{receiver_id}</code> @{receiver_username}\n\n\
📋 Complaint from: <code>{sender_id}</code> @{sender_username}\n\
📝 Reason: {reason}"
    else:
        await Complaint.update(session=session, id=complaint_id, status=ComplaintStatus.Rejected)
        text = "❌ Administrator <code>{admin_id}</code> @{admin_username} \
rejected the complaint against user <code>{receiver_id}</code> @{receiver_username}\n\n\
📋 Complaint from: <code>{sender_id}</code> @{sender_username}\n\
📝 Reason: {reason}"

    await callback.message.edit_text(
        text.format(
            admin_id=callback.from_user.id,
            admin_username=callback.from_user.username or "None",
            receiver_id=receiver_id,
            receiver_username=receiver_username or "None",
            sender_id=complaint.sender_id if complaint else "None",
            sender_username=sender_user.username
            if sender_user and sender_user.username
            else "None",
            reason=complaint.reason if complaint and complaint.reason else "No reason provided",
        ),
        parse_mode="HTML",
    )


def check_args_type(type: type, data_list: str) -> list | bool:
    try:
        return list(map(type, re.split(r"[ ,]+", data_list)))
    except:
        return False


def get_ban_text(is_banned: bool):
    text_success = (
        "✅ Send user IDs separated by ',' to ban users.\nExample: <code>/ban 123456, 789012</code>"
        if is_banned
        else "✅ Send user IDs separated by ',' to unban users.\nExample: <code>/unban 123456, 789012</code>"
    )

    text_action = "🔒 Banned" if is_banned else "🔓 Unbanned"
    text_error = "⚠️ Error while updating status"
    return text_success, text_action, text_error
