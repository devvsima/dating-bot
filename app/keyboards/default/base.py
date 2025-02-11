from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from loader import _

from .kb_generator import simple_kb_generator as kb_gen

del_kb = ReplyKeyboardRemove()


cancel_kb: ReplyKeyboardMarkup = kb_gen(
    ["/cancel"],
)

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
)

arhive_search_kb: ReplyKeyboardMarkup = kb_gen(
    ["❤️", "👎"],
    ["💤"],
)


def profile_return_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text=_("🔙 Вернуть профиль"))],
        ],
    )
    return kb


def report_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text="🔞"), KeyboardButton(text="💰"), KeyboardButton(text="🔫")],
            [KeyboardButton(text=_("Отменить жалобу"))],
        ],
    )
    return kb


def hints_kb(text: str) -> ReplyKeyboardMarkup:
    return kb_gen([text])


def leave_previous_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text=_("Оставить предыдущее"))],
        ],
    )
    return kb
