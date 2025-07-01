import asyncio

from aiogram import types
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from app.routers import admin_router
from app.states.admin import Mailing
from database.services.user import User


@admin_router.message(StateFilter(None), Command("mailing"))
async def users_mailing_panel(message: types.Message, state: FSMContext) -> None:
    """Admin panel for user mailing."""
    await message.answer(
        "📢 Send your message for mailing.\n"
        "You can send text, photo, video, or document. It will be forwarded to all users."
    )
    await state.set_state(Mailing.message)


@admin_router.message(StateFilter(Mailing.message))
async def start_mailing(message: types.Message, state: FSMContext, session) -> None:
    users = await User.get_all(session)
    sent_count, failed_count = 0, 0
    batch_size = 25  # чуть меньше лимита
    delay = 1  # секунда

    for i, user in enumerate(users, 1):
        try:
            await message.copy_to(chat_id=user.id, reply_markup=None)
            sent_count += 1
        except TelegramAPIError:
            failed_count += 1

        if i % batch_size == 0:
            await asyncio.sleep(delay)  # пауза после каждой пачки

    await message.answer(f"✅ Mailing completed!\n📬 Sent: {sent_count}\n⚠️ Failed: {failed_count}")
    await state.clear()
