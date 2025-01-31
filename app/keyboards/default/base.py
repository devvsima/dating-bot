from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)

from loader import _

from .kb_generator import simple_kb_generator as gen

del_kb = ReplyKeyboardRemove()

cancel_kb: ReplyKeyboardMarkup = gen(
    ["/cancel"]
)

profile_kb: ReplyKeyboardMarkup = gen(
    ["🔄", "🖼", "✍️", "❌"],
    ["🔍"]
)

menu_kb: ReplyKeyboardMarkup = gen(
    ["🔍", "👤", "🗄"],
    ["✉️"],
)

search_kb: ReplyKeyboardMarkup = gen(
    ["❤️", "💢", "👎"],
    ["💤"]
)

arhive_search_kb: ReplyKeyboardMarkup = gen(
    ["❤️", "👎"],
    ["💤"]
)


def profile_return_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=_("🔙 Вернуть профиль")),
            ],
        ],
        one_time_keyboard=True,
    )
    return kb

# async def report_kb() -> ReplyKeyboardMarkup:
#     kb = ReplyKeyboardMarkup(
#         resize_keyboard=True,
#             keyboard=[
#             [
#                 KeyboardButton(text="🔞"),
#                 KeyboardButton(text="💰"),
#                 KeyboardButton(text="🔫"),
#             ],
#             [
#                 KeyboardButton(text=_("Отменить жалобу")),
#             ],
#         ],
#     )
#     return kb
