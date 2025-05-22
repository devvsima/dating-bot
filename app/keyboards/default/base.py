from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from database.models.profile import ProfileModel
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
    ["🔍", "👤", "📭"],
    ["✉️"],
)

search_kb: ReplyKeyboardMarkup = kb_gen(
    ["❤️", "💢", "👎"],
    ["💤"],
)
