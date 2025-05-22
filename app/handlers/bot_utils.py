import html
import re

from app.handlers.message_text import user_message_text as umt
from app.keyboards.default.base import menu_kb
from app.keyboards.inline.admin import block_user_ikb
from app.keyboards.inline.archive import check_archive_ikb
from data.config import MODERATOR_GROUP
from database.models import ProfileModel, UserModel
from database.services import User
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


async def complaint_to_profile(user: UserModel, profile: ProfileModel, session) -> None:
    """Отправляет в группу модераторов анкету пользователя
    на которого пришла жалоба"""
    if MODERATOR_GROUP:
        try:
            await send_profile(MODERATOR_GROUP, profile)
            reported_user = await User.get_by_id(session, profile.id)

            text = umt.REPORT_TO_USER.format(
                user.id, user.username, profile.id, reported_user.username
            )

            await bot.send_message(
                chat_id=MODERATOR_GROUP,
                text=text,
                reply_markup=block_user_ikb(
                    id=profile.id,
                    username=reported_user.username,
                ),
            )
        except:
            logger.error("Сообщение в модераторскую группу не отправленно")


async def send_profile(chat_id: int, profile: ProfileModel) -> None:
    """Отправляет пользователю переданный в функцию профиль"""
    await bot.send_photo(
        chat_id=chat_id,
        photo=profile.photo,
        caption=f"{profile.name}, {profile.age}, {profile.city}\n{profile.description}",
        parse_mode=None,
    )


async def new_user_alert_to_group(user: UserModel) -> None:
    """Отправляет уведомление в модераторскуб группу о новом пользователе"""
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


from database.services.match import Match


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
