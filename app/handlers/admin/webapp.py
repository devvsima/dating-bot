from aiogram import F, types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.routers import admin_router
from data.config import webapp

"""
WebApp команды которые тестируются,
потому доступ пока только у админиматрсторов
"""


@admin_router.message(StateFilter(None), Command("webapp"))
async def webapp_menu(message: types.Message) -> None:
    """Открыть WebApp"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🌐 Открыть приложение", web_app=types.WebAppInfo(url=webapp.URL))

    await message.answer(
        "🚀 <b>Telegram WebApp</b>\n\nНажмите на кнопку ниже, чтобы открыть веб-приложение:",
        reply_markup=builder.as_markup(),
    )


@admin_router.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    """Обработка данных от WebApp"""
    data = message.web_app_data.data

    await message.answer(f"✅ Получены данные от WebApp:\n\n<code>{data}</code>")
