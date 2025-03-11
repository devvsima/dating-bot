from aiogram import F, types
from aiogram.filters.state import StateFilter

from app.handlers.message_text import admin_message_text as amt
from app.keyboards.default.admin import user_ban_or_unban_kb
from app.routers import admin_router as router


@router.message(F.text == "👤 Users", StateFilter(None))
async def _users_admin_panel(message: types.Message) -> None:
    """Админ панель управление пользователями"""
    await message.answer(
        text=amt.USER_PANEL,
        reply_markup=user_ban_or_unban_kb,
    )


@router.message(F.text == "⚔️ Ban users", StateFilter(None))
async def _ban_users_command(message: types.Message) -> None:
    """Запрашивает список пользоветелей которых нужно заблокировать"""
    await message.answer(amt.BAN_USERS_PANEL)


@router.message(F.text == "💊 Unban users", StateFilter(None))
async def _unban_users_commad(message: types.Message) -> None:
    """Запрашивает список пользоветелей которых нужно разблокировать"""
    await message.answer(amt.UNBAN_USERS_PANEL)


"""unfinished"""
