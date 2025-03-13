from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from loader import _, bot, i18n


def get_default_commands() -> list:
    commands = [
        BotCommand(command="/start", description="Start"),
        BotCommand(command="/lang", description="🌍 Change language"),
        BotCommand(command="/help", description="📝 Help & description"),
    ]

    return commands


def get_admins_commands() -> list:
    commands = get_default_commands()
    commands.extend(
        [
            BotCommand(command="/stats", description="📊 View statistics"),
            BotCommand(command="/mailing", description="📢 Send mailing to users"),
            BotCommand(command="/ban", description="⛔ Block user"),
            BotCommand(command="/unban", description="✅ Unblock user"),
            BotCommand(command="/log", description="📄 Send logs"),
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
