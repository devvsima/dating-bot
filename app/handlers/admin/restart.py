import os
import sys

from aiogram import types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from app.routers import admin_router


@admin_router.message(StateFilter(None), Command("restart"))
async def _restart_command(message: types.Message) -> None:
    await message.answer("Restarting and updating the bot...")
    os.system("git pull")
    os.execv(sys.executable, ["uv", "main.py"])
