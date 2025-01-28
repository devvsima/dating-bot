from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from app.routers import user_router as router

from app.handlers.bot_utils import menu
from app.others.states import DisableProfile

@router.message(F.text == "💤", StateFilter("*"))
@router.message(Command("cancel"), StateFilter("*"))
async def cancel_command(message: types.Message, state: FSMContext) -> None:
    """Сбрасывает состояния и дает пользователю меню"""
    if state is None:
        return
    if await state.get_state() == DisableProfile.waiting:
        return
    await state.clear()
    await menu(message.from_user.id)
