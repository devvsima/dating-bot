from aiogram import types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from app.routers import admin_router
from app.states.admin import PhotoId


@admin_router.message(StateFilter(None), Command("file_id"))
async def _photo_id_command(message: types.Message, state: FSMContext) -> None:
    """Админ панель"""
    await message.answer("Send your photo")
    await state.set_state(PhotoId.photo)


@admin_router.message(StateFilter(PhotoId.photo))
async def _get_photo_id_command(message: types.Message, state: FSMContext) -> None:
    """Админ панель"""
    if message.photo:
        photo_id = message.photo[-1].file_id
        await message.answer(f"<code>{photo_id}</code>")
        await state.clear()
        return
    await message.answer("Incorrect image")
