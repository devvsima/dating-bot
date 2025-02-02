from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)

from loader import _

from .kb_generator import simple_kb_generator as kb_gen

del_kb = ReplyKeyboardRemove()


cancel_kb: ReplyKeyboardMarkup = kb_gen(["/cancel"])

profile_kb: ReplyKeyboardMarkup = kb_gen(
    ["🔄", "🖼", "✍️", "❌"],
    ["🔍"],
)

menu_kb: ReplyKeyboardMarkup = kb_gen(
    ["🔍", "👤", "🗄"],
    ["✉️"],
)

search_kb: ReplyKeyboardMarkup = kb_gen(
    ["❤️", "💢", "👎"],
    ["💤"],
    one_time=False,
)

arhive_search_kb: ReplyKeyboardMarkup = kb_gen(
    ["❤️", "👎"],
    ["💤"],
    one_time=False,
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
