from loader import bot
from data.config import MODERATOR_GROUP
from utils.logging import logger

from database.models.users import Users
from database.models.profile import Profile

from app.handlers.msg_text import msg_text
from app.keyboards.default.base import menu_kb
from app.keyboards.inline.report import block_user_ikb


async def menu(user_id: int) -> None:
    """Отправляет меню пользователю"""
    await bot.send_message(
        chat_id = user_id, 
        text = msg_text.MENU, 
        reply_markup = menu_kb,
        )


async def report_to_profile(user, profile: Profile) -> None:
    """Отправляет в группу модераторов анкету пользователя
    на которого пришла жалоба"""
    if MODERATOR_GROUP:
        try:
            await send_profile(MODERATOR_GROUP, profile)
            text = msg_text.REPORT_TO_USER.format(user.username, user.id, profile.user_id.username, profile.user_id)
            
            await bot.send_message(
                chat_id = MODERATOR_GROUP,
                text = text,
                reply_markup = await block_user_ikb(profile.user_id),
                )
        except:
            logger.error("Сообщение в модераторскую группу не отправленно")
            
            
async def send_profile(user_id: int, profile: Profile) -> None:
    """Отправляет пользователю переданный в функцию профиль"""
    await bot.send_photo(
        chat_id = user_id,
        photo = profile.photo,
        caption = f"{profile.name}, {profile.age}, {profile.city}\n{profile.description}",
        parse_mode = None,
        )
    

async def new_user_alert_to_group(user: Users) -> None:
    """Отправляет уведомление в модераторскуб группу о новом пользователе"""    
    if MODERATOR_GROUP:
        try:            
            await bot.send_message(
            chat_id = MODERATOR_GROUP,
            text = msg_text.NEW_USER.format(user.username, user.id)
            )            
        except:
            logger.error("Сообщение в модераторскую группу не отправленно")


def generate_user_link(user_id: int, username: str = None) -> str:
    """
    Генерирует ссылку на пользователя
    Если указан username, создается ссылка https://t.me/username,
    иначе используется tg://user?id=user_id.
    """
    if username:
        return f"https://t.me/{username}"
    return f"tg://user?id={user_id}"


async def sending_user_contact(user_id: int, name: str, user_link: str) -> None:
    """Отправляет сообщение с контактом пользователя"""
    await bot.send_message(
        chat_id = user_id,
        text = msg_text.LIKE_ACCEPT.format(user_link, name),
    )