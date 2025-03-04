from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from loader import _, bot, i18n


def get_default_commands(lang: str = "en") -> list:
    commands = [
        BotCommand(command="/start", description=_("Начать", locale=lang)),
        BotCommand(command="/lang", description=_("Изменить язык бота", locale=lang)),
        BotCommand(command="/help", description=_("Дополнительное описание", locale=lang)),
        BotCommand(command="/activate", description=_("Активировать анкету", locale=lang)),
    ]

    return commands


def get_admins_commands(lang: str = "en") -> list:
    commands = get_default_commands(lang)
    commands.extend(
        [
            BotCommand(command="/admin", description=_("Админ панель", locale=lang)),
            BotCommand(command="/stats", description=_("Статистика", locale=lang)),
        ]
    )
    return commands


async def set_default_commands() -> None:
    await bot.set_my_commands(get_default_commands(), scope=BotCommandScopeDefault())
    for lang in i18n.available_locales:
        await bot.set_my_commands(
            get_default_commands(lang),
            scope=BotCommandScopeDefault(),
            language_code=lang,
        )


async def set_admins_commands(id: int) -> None:
    await bot.set_my_commands(get_admins_commands(), scope=BotCommandScopeChat(chat_id=id))
    for lang in i18n.available_locales:
        await bot.set_my_commands(
            get_admins_commands(lang),
            scope=BotCommandScopeChat(chat_id=id),
            language_code=lang,
        )
