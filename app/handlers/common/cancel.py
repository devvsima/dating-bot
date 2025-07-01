from aiogram import F, types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from app.business.menu_service import menu
from app.routers import common_router


@common_router.message(StateFilter("*"), F.text == "💤")
@common_router.message(StateFilter("*"), Command("cancel"))
async def cancel_command(message: types.Message, state: FSMContext) -> None:
    """Сбрасывает состояния и отправляет меню пользователю"""
    await state.clear()
    await menu(message.from_user.id)
