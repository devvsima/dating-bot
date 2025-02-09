from aiogram import F, types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from app.routers import user_router as router
from data.config import tgbot
from loader import bot

MODERATOR_GROUP = tgbot.MODERATOR_GROUP


@router.message(Command("sponsor"), StateFilter(None))
async def _sponsor_command(message: types.Message) -> None:
    """"""
    await message.answer_invoice(
        title="Стать спонсором",
        description="Небольшая поддержка бота дающая доступ в закрытую группу спонсоров",
        payload="sponsor",
        currency="XTR",
        prices=[types.LabeledPrice(label="XTR", amount=1)],
    )


@router.pre_checkout_query()
async def pre_checkout_query(event: types.PreCheckoutQuery) -> None:
    from utils.logging import logger

    logger.debug(event)
    await event.answer(True)


@router.message(F.succesful_payment.paylod == "sponsor")
async def succesful_payment(message: types.Message) -> None:
    link = await bot.create_chat_invite_link(MODERATOR_GROUP, member_limit=1)
    await bot.refund_star_payment(
        message.from_user.id, message.successful_payment.telegram_payment_charge_id
    )
    await message.answer(f"Твоя пригласительная ссылка: {link}")
