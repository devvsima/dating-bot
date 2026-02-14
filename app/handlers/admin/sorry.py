import asyncio

from aiogram import types
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest, TelegramForbiddenError
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.routers import admin_router
from database.models import Profile, User
from utils.logging import logger

# Клавиатура с кнопкой для изменения фото
edit_photo_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🖼")]], resize_keyboard=True)


@admin_router.message(StateFilter(None), Command("sorry_test"))
async def _sorry_test_command(message: types.Message, session: AsyncSession) -> None:
    """
    Тестовая команда для подсчета пользователей с профилем, но без фото.
    """
    # Получаем всех пользователей с их профилями и медиа
    result = await session.execute(
        select(User).options(joinedload(User.profile).selectinload(Profile.profile_media))
    )
    all_users = result.unique().scalars().all()

    # Фильтруем пользователей, у которых есть профиль, но нет фотографий
    users_with_profile_no_photo = [
        user
        for user in all_users
        if user.profile is not None and len(user.profile.profile_media) == 0
    ]

    await message.answer(
        f"Количество людей с профилем, но без фото: {len(users_with_profile_no_photo)}"
    )


@admin_router.message(StateFilter(None), Command("sorry"))
async def _sorry_command(message: types.Message, session: AsyncSession) -> None:
    """
    Команда для рассылки извинений пользователям с профилем, но без фото.
    Отправляет уведомление всем пользователям, у которых есть профиль, но нет фотографий.
    """
    # Получаем всех пользователей с их профилями и медиа
    result = await session.execute(
        select(User).options(joinedload(User.profile).selectinload(Profile.profile_media))
    )
    all_users = result.unique().scalars().all()

    # Фильтруем пользователей, у которых есть профиль, но нет фотографий
    users_with_profile_no_photo = [
        user
        for user in all_users
        if user.profile is not None and len(user.profile.profile_media) == 0
    ]

    if not users_with_profile_no_photo:
        await message.answer("❌ Нет пользователей с профилем без фото для рассылки.")
        return

    await message.answer(
        f"📨 Начинаю рассылку извинений...\n"
        f"👥 Пользователей с профилем без фото: {len(users_with_profile_no_photo)}"
    )

    sent_count, failed_count, blocked_count = 0, 0, 0
    batch_size = 25  # чуть меньше лимита Telegram API
    delay = 1  # секунда между пачками

    # Переводы сообщения для всех языков
    apology_texts = {
        "en": (
            "Hi! �\n\n"
            "We noticed your profile has no photo.\n"
            "There was a bug that prevented photos from being saved — sorry about that! 😔\n\n"
            "Please add your photo by clicking the 🖼 button below.\n\n"
        ),
        "es": (
            "¡Hola! 👋\n\n"
            "Notamos que tu perfil no tiene foto.\n"
            "Hubo un error que impedía guardar las fotos — ¡lo sentimos! 😔\n\n"
            "Por favor, añade tu foto haciendo clic en el botón 🖼 de abajo.\n\n"
        ),
        "fr": (
            "Salut ! 👋\n\n"
            "Nous avons remarqué que votre profil n'a pas de photo.\n"
            "Il y avait un bug qui empêchait l'enregistrement des photos — désolé ! 😔\n\n"
            "Veuillez ajouter votre photo en cliquant sur le bouton 🖼 ci-dessous.\n\n"
        ),
        "id": (
            "Hai! 👋\n\n"
            "Kami perhatikan profil Anda belum ada foto.\n"
            "Ada bug yang mencegah foto tersimpan — maaf ya! 😔\n\n"
            "Silakan tambahkan foto Anda dengan klik tombol 🖼 di bawah.\n\n"
        ),
        "pl": (
            "Cześć! 👋\n\n"
            "Zauważyliśmy, że Twój profil nie ma zdjęcia.\n"
            "Był błąd, który uniemożliwiał zapisanie zdjęć — przepraszamy! 😔\n\n"
            "Dodaj swoje zdjęcie, klikając przycisk 🖼 poniżej.\n\n"
        ),
        "ru": (
            "Привет! 👋\n\n"
            "Мы заметили, что в твоей анкете нет фотографии.\n"
            "Была ошибка, из-за которой фото не сохранялись — извини! 😔\n\n"
            "Пожалуйста, добавь свою фотографию, нажав кнопку 🖼 ниже.\n\n"
        ),
        "uk": (
            "Привіт! 👋\n\n"
            "Ми помітили, що в твоїй анкеті немає фотографії.\n"
            "Була помилка, через яку фото не зберігалися — вибач! 😔\n\n"
            "Будь ласка, додай своє фото, натиснувши кнопку 🖼 нижче.\n\n"
        ),
    }

    for i, user in enumerate(users_with_profile_no_photo, 1):
        # Выбираем текст в зависимости от языка пользователя
        apology_text = apology_texts.get(user.language, apology_texts["en"])

        try:
            await message.bot.send_message(
                chat_id=user.id, text=apology_text, reply_markup=edit_photo_kb
            )
            sent_count += 1
            logger.log("MAILING", f"Sent apology to user {user.id}")
        except TelegramForbiddenError:
            # Бот заблокирован пользователем
            blocked_count += 1
            logger.log("MAILING", f"User {user.id} blocked bot")
        except (TelegramBadRequest, TelegramAPIError) as e:
            # Другие ошибки (пользователь удален, чат не найден и т.д.)
            failed_count += 1
            logger.log("MAILING", f"Failed to send to user {user.id}: {e}")

        # Пауза после каждой пачки для соблюдения лимитов API
        if i % batch_size == 0:
            await asyncio.sleep(delay)

    # Итоговая статистика
    await message.answer(
        f"✅ <b>Рассылка завершена!</b>\n\n"
        f"📬 Отправлено: {sent_count}\n"
        f"🚫 Заблокировали бота: {blocked_count}\n"
        f"⚠️ Другие ошибки: {failed_count}\n\n"
        f"📊 Всего пользователей с профилем без фото: {len(users_with_profile_no_photo)}",
        parse_mode="HTML",
    )
