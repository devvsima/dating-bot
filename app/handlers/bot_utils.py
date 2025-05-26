import re

from aiogram.types import InputMediaPhoto

from app.handlers.message_text import user_message_text as umt
from app.keyboards.default.base import menu_kb
from app.keyboards.inline.admin import block_user_ikb
from app.keyboards.inline.archive import check_archive_ikb
from data.config import MODERATOR_GROUP
from database.models import ProfileModel, UserModel
from database.services.match import Match
from database.services.search import haversine_distance
from loader import bot
from utils.logging import logger

effect_dict_id = {
    "🔥": "5104841245755180586",
    "👍": "5107584321108051014",
    "👎": "5104858069142078462",
    "🎉": "5046509860389126442",
    "💩": "5046589136895476101",
}


def check_args_type(type: type, data_list: str) -> list | bool:
    try:
        return list(map(type, re.split(r"[ ,]+", data_list)))
    except:
        return False


async def menu(chat_id: int) -> None:
    """Отправляет меню пользователю"""
    await bot.send_message(
        chat_id=chat_id,
        text=umt.MENU,
        reply_markup=menu_kb,
    )


async def complaint_to_profile(
    complainant: UserModel, reason: str, complaint_profile: ProfileModel
) -> None:
    """Отправляет в группу модераторов анкету пользователя
    на которого пришла жалоба"""
    if MODERATOR_GROUP:
        try:
            await send_profile(MODERATOR_GROUP, complaint_profile)

            text = umt.REPORT_TO_USER.format(
                complainant.id,
                complainant.username,
                complaint_profile.id,
                complaint_profile.username,
                reason,
            )

            await bot.send_message(
                chat_id=MODERATOR_GROUP,
                text=text,
                reply_markup=block_user_ikb(
                    id=complaint_profile.id,
                    username=complaint_profile.username,
                ),
            )
        except:
            logger.error("Сообщение в модераторскую группу не отправленно")


async def send_profile(chat_id: int, profile: ProfileModel) -> None:
    """Отправляет профиль с несколькими фотографиями"""

    text = f"{profile.name}, {profile.age}, {profile.city}\n{profile.description}"
    media = [
        InputMediaPhoto(
            media=photo.photo,
            caption=text if i == 0 else None,
            parse_mode=None,
        )
        for i, photo in enumerate(profile.photos)
    ]
    await bot.send_media_group(chat_id=chat_id, media=media)


async def send_profile_with_dist(user: UserModel, profile: ProfileModel) -> None:
    """Отправляет профиль пользователя с расстоянием до него в киломтерах"""
    if profile.city == "📍":
        distance = haversine_distance(
            user.profile.latitude, user.profile.longitude, profile.latitude, profile.longitude
        )
        city = f"📍 {round(distance, 2)} km"
    else:
        city = profile.city
    text = f"{profile.name}, {profile.age}, {city}\n{profile.description}"

    media = [
        InputMediaPhoto(
            media=photo.photo,
            caption=text if i == 0 else None,
            parse_mode=None,
        )
        for i, photo in enumerate(profile.photos)
    ]
    await bot.send_media_group(chat_id=user.id, media=media)


async def new_user_alert_to_group(user: UserModel) -> None:
    """Отправляет уведомление в модераторскую группу о новом пользователе"""
    if MODERATOR_GROUP:
        try:
            await bot.send_message(
                chat_id=MODERATOR_GROUP,
                text="New user!\n<code>{}</code> (@{})".format(user.id, user.username),
            )
        except:
            logger.error("Сообщение в модераторскую группу не отправленно")


def generate_user_link(id: int, username: str = None) -> str:
    """
    Генерирует ссылку на пользователя
    Если указан username, создается ссылка https://t.me/username,
    иначе используется tg://user?id=id.
    """
    if username:
        return f"https://t.me/{username}"
    return f"tg://user?id={id}"


async def send_message_with_effect(
    chat_id: int, text: str, effect_id: str = effect_dict_id["🎉"]
) -> None:
    """Отправляет сообщение с контактом пользователя"""
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            message_effect_id=effect_id,
        )
    except:
        logger.info(
            f"Пользователю {chat_id} не удалось отправить контакт. Скорее всего пользователь заблокировал бота"
        )


async def send_user_like_alert(session, user: UserModel):
    matchs = await Match.get_user_matchs(session, user.id)
    try:
        await bot.send_message(
            chat_id=user.id,
            text=umt.LIKE_PROFILE(user.language).format(len(matchs)),
            reply_markup=check_archive_ikb(user.language),
        )
    except:
        logger.info(
            f"Пользователю {user.id} @{user.username}:\
            не было отправлнно оповещение, вероятно из за блокироваки бота"
        )
