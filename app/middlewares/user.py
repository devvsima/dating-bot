from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery, InlineQuery

from database.service.users import get_or_create_user, get_user, create_user, new_referral



class UsersMiddleware(BaseMiddleware):
    @staticmethod
    async def on_process_message(message: Message, data: dict[str]):
        if 'channel_post' in message or message.chat.type != 'private':
            raise CancelHandler()

        await message.answer_chat_action('typing')

        user = get_user(message.from_user.id)
        if message.text:
            if message.text.startswith('/start'):
                if not user:
                    user = create_user(message.from_user.id, message.from_user.username, message.from_user.language_code)
                    from app.handlers.bot_utils import new_user_alert_to_group
                    
                    await new_user_alert_to_group(user)
                    inviter = get_user(message.get_args())
                    if inviter:
                        new_referral(inviter)
        if user.is_banned:
            raise CancelHandler()
        data['user'] = user

    @staticmethod
    async def on_process_callback_query(callback_query: CallbackQuery, data: dict[str]):
        user = callback_query.from_user

        data['user'] = get_or_create_user(user.id, user.username, user.language_code)

    @staticmethod
    async def on_process_inline_query(inline_query: InlineQuery, data: dict[str]):
        user = inline_query.from_user

        data['user'] = get_or_create_user(user.id, user.username, user.language_code)