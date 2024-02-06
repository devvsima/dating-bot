from aiogram.types import BotCommandScopeDefault, BotCommandScopeChat, BotCommand

from loader import bot

admin_commands = [
        BotCommand('/admin', 'example'),
    ]

async def set_admin_commands(user_id: int):
    await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(user_id))
