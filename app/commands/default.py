from aiogram.types import BotCommandScopeDefault, BotCommandScopeChat, BotCommand

from loader import bot

async def set_default_commands():
    commands = [
        BotCommand('/start', 'start bot'),
        BotCommand('/help', 'how it works?'),
        BotCommand('/lang', 'change language'),
        BotCommand('/settings', 'open bot settings'),
    ]

    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())

