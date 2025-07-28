from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from loader import _

from .kb_generator import simple_kb_generator as kb_gen

del_kb = ReplyKeyboardRemove()


cancel_kb: ReplyKeyboardMarkup = kb_gen(
    ["/cancel"],
)

start_kb: ReplyKeyboardMarkup = kb_gen(
    ["/start"],
)

profile_kb: ReplyKeyboardMarkup = kb_gen(
    ["🔄", "🖼", "✍️", "❌"],
    ["↩️"],
)

menu_kb: ReplyKeyboardMarkup = kb_gen(
    ["🔍", "👤", "📭"],
    ["✉️"],
)

search_kb: ReplyKeyboardMarkup = kb_gen(
    ["❤️", "📩", "👎"],
    ["💢"],
    ["💤"],
)

match_kb: ReplyKeyboardMarkup = kb_gen(
    ["❤️", "👎"],
    ["💢"],
    ["💤"],
)

return_to_menu_kb: ReplyKeyboardMarkup = kb_gen(
    ["↩️"],
)
