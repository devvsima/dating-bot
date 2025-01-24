from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from loader import _, bot, i18n


def get_default_commands(lang: str = "en"):
    commands = [
        BotCommand(command="/start", description=_("start chat", locale=lang)),
        BotCommand(command="/lang", description=_("change language", locale=lang)),
        BotCommand(command="/help", description=_("additional description", locale=lang)),
    ]

    return commands

def get_admins_commands(lang: str = "en"):
    commands = get_default_commands(lang)
    commands.extend(
        [
            BotCommand(
                command="/admin", description=_("admin panel", locale=lang)
            )
        ]
    )
    return commands


async def set_default_commands():
    await bot.set_my_commands(get_default_commands(), scope=BotCommandScopeDefault())
    for lang in i18n.available_locales:
        await bot.set_my_commands(
            get_default_commands(lang),
            scope=BotCommandScopeDefault(),
            language_code=lang,
        )

async def set_admins_commands(id: int):
    await bot.set_my_commands(
        get_admins_commands(), scope=BotCommandScopeChat(chat_id=id)
    )
    for lang in i18n.available_locales:
        await bot.set_my_commands(
            get_admins_commands(lang),
            scope=BotCommandScopeChat(chat_id=id),
            language_code=lang,
        )