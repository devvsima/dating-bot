from core.config import SUPPORT_COST
from core.loader import _

"""
Текста много и он может повторятся, потому вынес его в отдельный файл.
"""


class MessageText:
    @property
    def WELCOME(self):
        return _("""
Привет! 👋

Добро пожаловать в наш бот знакомств Michi! 💕
Чтобы начать, создай свой профиль — это просто и быстро.

Желаем тебе приятных знакомств и интересных встреч!
""")

    @property
    def INFO(self):
        return _("""
👋
Немного информации о боте:
Этот бот был создан по аналогии с популярным ботом для знакомств <a href='https://t.me/leomatchbot?start=i_VwRd0'>Дайвинчик</a>
Весь код бота открыт и доступен на <a href='https://github.com/devvsima/dating-bot'>GitHub</a>

По вопросам и предложениям можно писать сюда: @devvsima.
""")

    @property
    def MENU(self):
        return _("""
🔍 Смотреть анкеты
👤 Моя анкета
📭 Кто меня лайкнул

✉️ Пригласить друзей""")

    @property
    def PROFILE_MENU(self):
        return _("""
🔄 Заполнить анкету заново
🖼 Изменить фотографию
✍️ Изменить описание
❌ Отключить анкету

↩️ Назад
""")

    # @property
    def UNKNOWN_COMMAND(self, language: str = "en"):
        return _(
            "Неизвестная команда. Если заблудился, напиши /start.",
            locale=language,
        )

    # Создание и редактирование профиля
    @property
    def GENDER(self):
        return _("Укажи, свой пол: 👤")

    @property
    def FIND_GENDER(self):
        return _("Выбери, кого ты ищешь: 💕")

    @property
    def PHOTO(self):
        return _("Загрузи своё фото! Можно отправить до 3 фотографий одновременно 📸")

    @property
    def NAME(self):
        return _("Как тебя зовут? ✍️")

    @property
    def AGE(self):
        return _("Сколько тебе лет? 🎂")

    @property
    def CITY(self):
        return _("Укажи свой город: 🏙️")

    @property
    def DESCRIPTION(self):
        return _("Расскажи немного о себе — это поможет другим узнать тебя лучше! 📝")

    @property
    def PROFILE_CREATED(self):
        return _("Отлично! Твой профиль готов — теперь можешь искать интересных для себя людей 💬")

    @property
    def DISABLE_PROFILE(self):
        return _("""
❌ Твоя анкета отключена, некоторые функции теперь недоступны.
💬 Чтобы снова активировать анкету, отправь команду /start.""")

    @property
    def ACTIVATE_PROFILE_ALERT(self):
        return _("✅ Твоя анкета успешно восстановлена! Теперь ты снова можешь пользоваться ботом.")

    @property
    def SEARCH(self):
        return _("🔍 Выполняется поиск...")

    @property
    def ARCHIVE_SEARCH(self):
        return _("Твоя анкета понравилась {} людям! Давай посмотрим, кто это:")

    @property
    def INVALID_PROFILE_SEARCH(self):
        return _("Подходящих анкет не найдено. Попробуй выбрать другой город. 🌍")

    @property
    def EMPTY_PROFILE_SEARCH(self):
        return _("Анкеты закончились. Попробуй позже! 😊")

    def LIKE_PROFILE(self, language: str):
        return _(
            "Твоя анкета получила <b>{}</b> ❤️\n\n📭 Нажми, чтобы посмотреть",
            locale=language,
        )

    @property
    def LIKE_ARCHIVE(self):
        return _("Пока никто не поставил тебе лайк, но всё ещё впереди!")

    def LIKE_ACCEPT(self, language: str):
        return _(
            "Надеюсь вы хорошо проведете время ;) <a href='{}'>{}</a>",
            locale=language,
        )

    # @property
    # def LIKE_ACCEPT_ALERT(self):
    #     return _(
    #         "На ваш лайк ответили взаимно, надеюсь вы хорошо проведете время ;) <a href='{}'>{}</a>",
    #     )

    @property
    def MESSAGE_TO_YOU(self):
        return _("Сообщение для тебя:\n{}")

    @property
    def MAILING_TO_USER(self):
        return _(
            "Можешь написать пользователю, до 250 символов. ✉️\n\nЕсли не хочешь писать, нажми на кнопку ниже."
        )

    @property
    def MAILING_LIKE(self):
        return _("Отправил сообщение, ждем ответа.")

    @property
    def INVALID_MAILING_TO_USER(self):
        return _("Не корректное сообщение. Пожалуйста, напиши до 250 символов.")

    @property
    def CANNCELED_LETTER(self):
        return _("Хорошо, ничего не буду отправлять.")

    # Ошибки и проверки
    @property
    def INVALID_RESPONSE(self):
        return _("Некорректный ответ. Пожалуйста, выбери на клавиатуре или напиши правильно. 📝")

    @property
    def INVALID_DESCIPTION(self):
        return _("Превышен лимит символов. Пожалуйста, сократи сообщение. ✂️")

    @property
    def INVALID_NAME(self):
        return _("Некорректное имя. Имя должно содержать минимум 2 буквы и максимум 70 символов. ✍️")

    @property
    def INVALID_CITY_RESPONSE(self):
        return _("Такой город не найден 😔")

    @property
    def INVALID_PHOTO(self):
        return _(
            "Неверный формат фотографии! Пожалуйста, загрузите изображение в правильном формате. 🖼️"
        )

    @property
    def INVALID_AGE(self):
        return _("Неверный формат, возраст нужно указывать цифрами. 🔢")

    @property
    def INVITE_FRIENDS(self):
        return _(
            "Приглашай друзей и получай бонусы!\n\nПриглашенные пользователи: <b>{}</b>\n\nСсылка для друзей:\n<code>{}</code>"
        )

    @property
    def CHANNEL(self):
        return _("Наш канал:\n{}")

    # Язык
    @property
    def CHANGE_LANG(self):
        return _("Выбери язык бота, на который хочешь переключиться: 🌐")

    def DONE_CHANGE_LANG(self, language: str):
        return _("Язык бота изменён! ✅", locale=language)

    # Жалобы и модерация
    @property
    def COMPLAINT(self):
        return _("""
Укажи причину жалобы:
🔞 Неприличный контент
💰 Реклама
🔫 Другое

↩️ Назад
""")

    @property
    def REPORT_TO_USER(self):
        return """
User <code>{}</code> (@{}) sent a complaint
about a user profile: <code>{}</code> (@{})

The reason: {}
"""

    @property
    def REPORT_TO_PROFILE(self):
        return _("✅ Жалоба успешно отправлена на рассмотрение!")

    # Редактирование фотографий
    @property
    def PHOTO_EDIT_START(self):
        return _("Загрузи новые фото! Можно отправить до 3 фотографий 📸")

    @property
    def PHOTO_UNCHANGED(self):
        return _("Фотографии остались без изменений")

    @property
    def PHOTO_NO_UPLOADED(self):
        return _("Вы не загрузили ни одного фото. Попробуйте еще раз.")

    @property
    def PHOTO_SAVE_ERROR(self):
        return _("❌ Ошибка при сохранении фото. Попробуйте еще раз.")

    @property
    def PHOTO_SAVE_FINISH_BUTTON(self):
        return _("Это все, сохранить фото")

    @property
    def PHOTO_PROGRESS_TEMPLATE(self):
        return _(
            "📸 Фото {current}/{total} загружено!\n\nМожете загрузить еще {remaining} фото или нажать '{finish_button}'"
        )

    def PHOTO_PROGRESS(self, current: int, total: int = 3):
        remaining = total - current
        finish_button_text = _("Это все, сохранить фото")
        return self.PHOTO_PROGRESS_TEMPLATE.format(
            current=current, total=total, remaining=remaining, finish_button=finish_button_text
        )

    def PHOTO_SAVED(self, count: int):
        return _("Сохранено {} фото!").format(count)

    def PHOTO_ALL_UPLOADED(self, count: int = 3):
        return _("Все {} фото загружены!").format(count)

    @property
    def PHOTO_LIMIT_REACHED(self):
        return _("❌ Максимум 3 фото! Нажмите 'Это все, сохранить фото' для сохранения.")

    @property
    def PHOTO_UPLOAD_INSTRUCTION(self):
        return _("📸 Отправьте фотографию или выберите действие из меню")

    @property
    def PHOTO_REQUIRED_FOR_PROFILE(self):
        return _("❌ Для создания профиля необходимо загрузить хотя бы одно фото!")

    def RATE_LIMIT_MESSAGE(self, language: str = "en"):
        return _(
            "⏳ Вы отправляете сообщения слишком часто. Пожалуйста, подождите пару секунд.",
            locale=language,
        )

    @property
    def PAYMENT_TITEL(self):
        return _("Поддержка проекта")

    @property
    def PAYMENT_DESCRIPTION(self):
        return _(f"Поддержи проект на {SUPPORT_COST} звёзд и помоги ему развиваться дальше ✨")


message_text = MessageText()
