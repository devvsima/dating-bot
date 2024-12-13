from aiogram.types import BotCommandScopeDefault, BotCommandScopeChat, BotCommand

from loader import bot

admin_commands = [
        BotCommand('/admin', 'admin panel'),
        BotCommand('/reg', 'bot send regestration graph'),
    ]

async def set_admin_commands(user_id: int):
    await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(user_id))
