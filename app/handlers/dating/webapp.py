"""
Обработчик для открытия WebApp
"""

from aiogram import F, types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.keyboards.default.webapp import webapp_test_kb
from app.routers import dating_router
from data.config import webapp


@dating_router.message(StateFilter(None), Command("webapp"))
async def webapp_menu(message: types.Message) -> None:
    """Меню WebApp"""

    await message.answer(
        "📱 <b>WebApp меню</b>\n\nИспользуй кнопку ниже для открытия веб-приложения:",
        reply_markup=webapp_test_kb(),
    )


@dating_router.message(F.text == "🚀 Открыть WebApp")
async def open_webapp(message: types.Message):
    """Открыть WebApp"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🌐 Открыть приложение", web_app=types.WebAppInfo(url=webapp.URL))

    await message.answer(
        "🚀 <b>Telegram WebApp</b>\n\nНажмите на кнопку ниже, чтобы открыть веб-приложение:",
        reply_markup=builder.as_markup(),
    )


@dating_router.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    """Обработка данных от WebApp"""
    data = message.web_app_data.data

    await message.answer(f"✅ Получены данные от WebApp:\n\n<code>{data}</code>")
