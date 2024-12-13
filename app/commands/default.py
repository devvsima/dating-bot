from aiogram.types import BotCommandScopeDefault, BotCommand

from loader import bot

async def set_default_commands():
    commands = [
        # BotCommand('/start', 'start bot'),
        BotCommand('/help', 'how it works?'),
        BotCommand('/lang', 'change language'),
        BotCommand('/profile', 'check your profile'),
        # BotCommand('/report', 'complain about a user'),
    ]

    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())

