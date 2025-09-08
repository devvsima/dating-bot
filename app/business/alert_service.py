from app.constans import REFERAL_SOURCES
from data.config import tgbot
from database.models.user import UserModel
from loader import bot
from utils.logging import logger

IS_ALERT = tgbot.NEW_USER_ALET_TO_GROUP
GROUP_ID = tgbot.MODERATOR_GROUP_ID


async def new_user_alert_to_group(user: UserModel, code: str) -> None:
    """Отправляет уведомление в модераторскую группу о новом пользователе"""
    if IS_ALERT and GROUP_ID:
        try:
            text = "New user!\n<code>{}</code> (@{})".format(user.id, user.username)
            if code:
                text += "\n\nSource: {}".format(REFERAL_SOURCES[code])
            await bot.send_message(chat_id=tgbot.MODERATOR_GROUP_ID, text=text)
        except:
            logger.error("Сообщение в модераторскую группу не отправленно")
