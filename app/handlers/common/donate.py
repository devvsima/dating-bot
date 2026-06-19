from aiogram import F
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.inline.payments import payment_ikb
from app.routers import common_router
from app.text import message_text as mt
from core.config import SUPPORT_COST
from database.models.user import User


@common_router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@common_router.callback_query(F.data == "donate")
async def send_invoice_handler(callback: CallbackQuery):
    prices = [LabeledPrice(label="XTR", amount=SUPPORT_COST)]
    title = mt.PAYMENT_TITEL
    description = mt.PAYMENT_DESCRIPTION
    await callback.answer()
    await callback.message.answer_invoice(
        title=title,
        description=description,
        prices=prices,
        provider_token="",
        payload="channel_support",
        currency="XTR",
        reply_markup=payment_ikb(),
    )


@common_router.message(F.successful_payment)
async def success_payment_handler(message: Message, user: User, session: AsyncSession):
    await User.update(
        session,
        user.id,
        status=2 if user.status <= 1 else user.status,
        stars=(user.stars or 0) + SUPPORT_COST,
    )
    await message.answer(text="🥳Спасибо за вашу поддержку проекта!🤗")
