from aiogram import F, types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from app.routers import admin_router
from data.config import tgbot, webapp


@admin_router.message(StateFilter(None), Command("webadmin"))
@admin_router.message(StateFilter(None), F.text == "🌐 Web Admin")
async def web_admin_command(message: types.Message) -> None:
    """Opens web admin panel in Telegram Web App"""

    # Check if user is administrator
    if message.from_user.id not in tgbot.ADMINS:
        await message.answer("❌ You don't have access to the admin panel.")
        return

    # Create inline keyboard with Web App

    # Create inline keyboard with Web App
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="🌐 Open Admin Panel",
                    web_app=types.WebAppInfo(url=webapp.URL),
                )
            ],
            [types.InlineKeyboardButton(text="🔗 Open in Browser", url=webapp.URL)],
        ]
    )

    await message.answer(
        text="📊 <b>Dating Bot Admin Panel</b>\n\n"
        "Choose how to open the web admin:\n\n"
        "🌐 <b>Web App</b> - opens inside Telegram\n"
        "🔗 <b>Browser</b> - opens in external browser",
        reply_markup=keyboard,
        parse_mode="HTML",
    )
