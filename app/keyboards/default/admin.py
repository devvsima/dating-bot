from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.keyboards.default.kb_generator import simple_kb_generator as kb_gen
from loader import _

admin_menu_kb: ReplyKeyboardMarkup = kb_gen(
    ["📊 Statistics"],
    ["👤 Users"],
    ["📩 Mailing to users"],
)

user_ban_or_unban_kb: ReplyKeyboardMarkup = kb_gen(
    ["⚔️ Ban users"],
    ["💊 Unban users"],
)
