from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from database.models.profile import ProfileModel
from database.models.user import UserModel
from loader import _

from .base import del_kb
from .kb_generator import simple_kb_generator as kb_gen


def create_profile_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=_("Создать анкету")),
            ],
        ],
    )
    return kb


class RegistrationFormKb:
    @staticmethod
    def gender() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text=_("Парень")), KeyboardButton(text=_("Девушка"))],
            ],
        )
        return kb

    @staticmethod
    def find_gender() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text=_("Парней")),
                    KeyboardButton(text=_("Девушек")),
                    KeyboardButton(text=_("Всех")),
                ],
            ],
        )
        return kb

    @staticmethod
    def photo(user) -> ReplyKeyboardMarkup:
        return RegistrationFormKb.leave_previous(user.profile)

    @staticmethod
    def age(user) -> ReplyKeyboardMarkup:
        try:
            kb = kb_gen([str(user.profile.age)])
        except:
            kb = del_kb
        return kb

    @staticmethod
    def name(user: UserModel) -> ReplyKeyboardMarkup:
        try:
            kb = kb_gen([user.profile.name])
        except:
            kb = del_kb
        return kb

    @staticmethod
    def description(user) -> ReplyKeyboardMarkup:
        return RegistrationFormKb.leave_previous(user.profile)

    @staticmethod
    def location(user: UserModel | None):
        builder = ReplyKeyboardBuilder()
        if user.profile and user.profile.city != "📍":
            builder.button(text=_("Оставить предыдущее"))
        builder.button(
            text=_("📍 Отправить местоположение"),
            request_location=True,
        )
        builder.adjust(1)
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def leave_previous(profile: ProfileModel) -> ReplyKeyboardMarkup:
        if profile:
            kb = ReplyKeyboardMarkup(
                resize_keyboard=True,
                one_time_keyboard=True,
                keyboard=[
                    [KeyboardButton(text=_("Оставить предыдущее"))],
                ],
            )
        else:
            kb = del_kb
        return kb
