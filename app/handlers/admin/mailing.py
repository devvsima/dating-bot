from aiogram import F, types
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from app.others.states import Mailing
from app.routers import admin_router as router
from database.services.user import User
from loader import bot


@router.message(Command("mailing"), StateFilter(None))
async def users_mailing_panel(message: types.Message, state: FSMContext) -> None:
    """Admin panel for user mailing."""
    await message.answer(
        "📢 Send your message for mailing.\n"
        "You can send text, photo, video, or document. It will be forwarded to all users."
    )
    await state.set_state(Mailing.message)


@router.message(StateFilter(Mailing.message))
async def start_mailing(message: types.Message, session) -> None:
    """Starts mailing to all users with text and media support."""
    users = await User.get_all(session)
    sent_count, failed_count = 0, 0

    for user in users:
        try:
            if message.text:
                await bot.send_message(user.id, message.text)
            elif message.photo:
                await bot.send_photo(user.id, message.photo[-1].file_id, caption=message.caption)
            elif message.video:
                await bot.send_video(user.id, message.video.file_id, caption=message.caption)
            elif message.document:
                await bot.send_document(user.id, message.document.file_id, caption=message.caption)
            else:
                continue

            sent_count += 1
        except TelegramAPIError:
            failed_count += 1

    await message.answer(f"✅ Mailing completed!\n📬 Sent: {sent_count}\n⚠️ Failed: {failed_count}")
