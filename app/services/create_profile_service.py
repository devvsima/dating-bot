from aiogram.types import Message

from app.filters.create_profile_filtres import LEAVE_PREVIOUS_OPTIONS, SKIP_OPTIONS
from database.models.user import UserModel


def get_correct_description(message: Message, user: UserModel):
    "Возвращает коректно описание профиля при заполнении формы"
    if message.text in SKIP_OPTIONS:
        description = ""
    elif message.text in LEAVE_PREVIOUS_OPTIONS and user.profile:
        description = user.profile.description
    else:
        description = message.text
    return description
