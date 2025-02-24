from aiogram import F, types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from app.handlers.bot_utils import menu
from app.others.states import LikeResponse, Search
from app.routers import user_router as router

LikeResponse


@router.message(F.text == "💤", StateFilter(Search.search, LikeResponse.response))
@router.message(Command("cancel"), StateFilter(Search.search, LikeResponse.response))
async def cancel_command(message: types.Message, state: FSMContext) -> None:
    """Сбрасывает состояния и дает пользователю меню"""
    await state.clear()
    await menu(message.from_user.id)
