from aiogram import F, types

from app.routers import admin_router as router

from app.filters.admin import IsAdmin
from app.handlers.msg_text import msg_text

from app.keyboards.default.admin import user_ban_or_unban_kb


@router.message(IsAdmin(), F.text.in_(["👤 Пользователи", "👤 Користувачі", "👤 Users"]))
async def _users_admin_panel(message: types.Message) -> None:
    """Админ панель управление пользователями"""
    await message.answer(msg_text.USER_PANEL, reply_markup=user_ban_or_unban_kb())


@router.message(IsAdmin(), F.text.in_(["⚔️ Забанить пользователей", "⚔️ Забанити користувачів", "⚔️ Ban users"]))
async def _ban_users_command(message: types.Message) -> None:
    """Запрашивает список пользоветелей которых нужно заблокировать"""
    await message.answer(msg_text.BAN_USERS_PANEL)


@router.message(IsAdmin(), F.text.in_(["💊 Разбанить пользователей", "💊 Розбанити користувачів", "💊 Unban users"]))
async def _unban_users_commad(message: types.Message) -> None:
    """Запрашивает список пользоветелей которых нужно разблокировать"""
    await message.answer(msg_text.UNBAN_USERS_PANEL)


"""unfinished"""
