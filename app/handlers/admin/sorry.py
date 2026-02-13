import asyncio

from aiogram import types
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest, TelegramForbiddenError
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.keyboards.default.base import start_kb
from app.routers import admin_router
from database.models import User
from utils.logging import logger


@admin_router.message(StateFilter(None), Command("sorry_test"))
async def _sorry_command(message: types.Message, session: AsyncSession) -> None:
    """
    Команда для рассылки извинений пользователям без профиля.
    Отправляет уведомление всем пользователям, у которых нет профиля.
    """
    # Получаем всех пользователей с их профилями
    result = await session.execute(select(User).options(joinedload(User.profile)))
    all_users = result.unique().scalars().all()
    users_without_profile = [user for user in all_users if user.profile is None]

    await message.answer(f"Количество людей: {len(users_without_profile)}")


@admin_router.message(StateFilter(None), Command("sorry"))
async def _sorry_command(message: types.Message, session: AsyncSession) -> None:
    """
    Команда для рассылки извинений пользователям без профиля.
    Отправляет уведомление всем пользователям, у которых нет профиля.
    """
    # Получаем всех пользователей с их профилями
    result = await session.execute(select(User).options(joinedload(User.profile)))
    all_users = result.unique().scalars().all()

    # Фильтруем пользователей без профиля
    users_without_profile = [user for user in all_users if user.profile is None]

    if not users_without_profile:
        await message.answer("❌ Нет пользователей без профиля для рассылки.")
        return

    await message.answer(
        f"📨 Начинаю рассылку извинений...\n"
        f"👥 Пользователей без профиля: {len(users_without_profile)}"
    )

    sent_count, failed_count, blocked_count = 0, 0, 0
    batch_size = 25  # чуть меньше лимита Telegram API
    delay = 1  # секунда между пачками

    # Переводы сообщения для всех языков
    apology_texts = {
        "en": (
            "Hi! 😊\n\n"
            "Previously, the bot had issues with profile registration — we apologize for the inconvenience.\n"
            "Everything is fixed now, you can try again 💪\n\n"
            "Click the button below or send /start command to create your profile.\n\n"
            "You can change language with /lang command 🌍"
        ),
        "es": (
            "¡Hola! 😊\n\n"
            "Anteriormente, el bot tenía problemas con el registro de perfiles — nos disculpamos por las molestias.\n"
            "Todo está arreglado ahora, puedes intentarlo de nuevo 💪\n\n"
            "Haz clic en el botón de abajo o envía el comando /start para crear tu perfil.\n\n"
            "Puedes cambiar el idioma con el comando /lang 🌍"
        ),
        "fr": (
            "Salut ! 😊\n\n"
            "Auparavant, le bot avait des problèmes avec l'enregistrement des profils — nous nous excusons pour le désagrément.\n"
            "Tout est corrigé maintenant, vous pouvez réessayer 💪\n\n"
            "Cliquez sur le bouton ci-dessous ou envoyez la commande /start pour créer votre profil.\n\n"
            "Vous pouvez changer la langue avec la commande /lang 🌍"
        ),
        "id": (
            "Hai! 😊\n\n"
            "Sebelumnya, bot mengalami masalah dengan pendaftaran profil — kami mohon maaf atas ketidaknyamanannya.\n"
            "Semuanya sudah diperbaiki sekarang, Anda bisa mencoba lagi 💪\n\n"
            "Klik tombol di bawah atau kirim perintah /start untuk membuat profil Anda.\n\n"
            "Anda dapat mengubah bahasa dengan perintah /lang 🌍"
        ),
        "pl": (
            "Cześć! 😊\n\n"
            "Wcześniej bot miał problemy z rejestracją profili — przepraszamy za niedogodności.\n"
            "Teraz wszystko działa, możesz spróbować ponownie 💪\n\n"
            "Kliknij przycisk poniżej lub wyślij komendę /start, aby utworzyć swój profil.\n\n"
            "Możesz zmienić język komendą /lang 🌍"
        ),
        "ru": (
            "Привет! 😊\n\n"
            "Раньше в боте были проблемы с регистрацией анкет — извиняемся за неудобства.\n"
            "Сейчас всё исправлено, можете попробовать снова 💪\n\n"
            "Нажмите кнопку ниже или отправьте команду /start, чтобы создать анкету.\n\n"
            "Язык можно изменить командой /lang 🌍"
        ),
        "uk": (
            "Привіт! 😊\n\n"
            "Раніше в боті були проблеми з реєстрацією анкет — вибачаємося за незручності.\n"
            "Зараз усе виправлено, можете спробувати знову 💪\n\n"
            "Натисніть кнопку нижче або надішліть команду /start, щоб створити анкету.\n\n"
            "Мову можна змінити командою /lang 🌍"
        ),
    }

    for i, user in enumerate(users_without_profile, 1):
        # Выбираем текст в зависимости от языка пользователя
        apology_text = apology_texts.get(user.language, apology_texts["en"])

        try:
            await message.bot.send_message(
                chat_id=user.id, text=apology_text, reply_markup=start_kb
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
        f"📊 Всего пользователей без профиля: {len(users_without_profile)}",
        parse_mode="HTML",
    )
