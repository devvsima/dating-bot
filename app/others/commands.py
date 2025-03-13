from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from loader import _, bot, i18n


def get_default_commands() -> list:
    commands = [
        BotCommand(command="/start", description="Start"),
        BotCommand(command="/lang", description="Change language"),
        BotCommand(command="/help", description="Help"),
        BotCommand(command="/cancel", description="Cancel"),
    ]

    return commands


def get_admins_commands() -> list:
    commands = get_default_commands()
    commands.extend(
        [
            BotCommand(command="/stats", description="Stats"),
            BotCommand(command="/mailing", description="Mailing"),
            BotCommand(command="/ban", description="Ban user"),
            BotCommand(command="/unban", description="Unban user"),
            BotCommand(command="/log", description="Logs"),
        ]
    )
    return commands


async def set_default_commands() -> None:
    await bot.set_my_commands(get_default_commands(), scope=BotCommandScopeDefault())
    for lang in i18n.available_locales:
        await bot.set_my_commands(
            get_default_commands(),
            scope=BotCommandScopeDefault(),
            language_code=lang,
        )


async def set_admins_commands(id: int) -> None:
    await bot.set_my_commands(get_admins_commands(), scope=BotCommandScopeChat(chat_id=id))
    for lang in i18n.available_locales:
        await bot.set_my_commands(
            get_admins_commands(),
            scope=BotCommandScopeChat(chat_id=id),
            language_code=lang,
        )
