from app.constans import REFERAL_SOURCES
from data.config import MODERATOR_GROUP, NEW_USER_ALET_TO_GROUP
from database.models.user import UserModel
from loader import bot
from utils.logging import logger


async def new_user_alert_to_group(user: UserModel, code: str) -> None:
    """Отправляет уведомление в модераторскую группу о новом пользователе"""
    if NEW_USER_ALET_TO_GROUP and MODERATOR_GROUP:
        try:
            text = "New user!\n<code>{}</code> (@{})".format(user.id, user.username)
            if code:
                text += "\n\nSource: {}".format(REFERAL_SOURCES[code])
            await bot.send_message(chat_id=MODERATOR_GROUP, text=text)
        except:
            logger.error("Сообщение в модераторскую группу не отправленно")
