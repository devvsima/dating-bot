from loader import _

"""
Текст вынес в отдельный файл для более удобного редактирования
"""


class MsgText:
    @property
    def WELCOME(self):
        return _(
            """
Привет! 👋

Добро пожаловать в наш Telegram-бот для знакомств! 💕
Чтобы начать, создай свой профиль 🚀

Желаем приятных знакомств! 😊
"""
        )

    @property
    def MENU(self):
        return _(
            """
🔍 Смотреть анкеты
👤 Моя анкета
🗄 Посмотреть лайки

✉️ Пригласить друзей"""
        )

    @property
    def PROFILE_MENU(self):
        return _(
            """
🔄 Заполнить анкету заново
🖼 Изменить фотографию
✍️ Изменить описание
❌ Отключить анкету

🔍 Смотреть анкеты
"""
        )

    @property
    def INFO(self):
        return _(
            """
👋
Немного информации о боте:
Этот бот был создан по аналогии с популярным ботом для знакомств <a href='https://t.me/leomatchbot?start=i_VwRd0'>Дайвинчик</a>
Весь код бота открыт и доступен на <a href='https://github.com/devvsima/dating-bot'>GitHub</a>

По вопросам и предложениям можно писать сюда: @devvsima.
"""
        )

    @property
    def SEARCH(self):
        return _("🔍 Выполняется поиск...")

    @property
    def INVALID_PROFILE_SEARCH(self):
        return _("Подходящих анкет нет. Попробуй указать другой город. 🌍")

    @property
    def EMPTY_PROFILE_SEARCH(self):
        return _("Больше анкет нет. Попробуйте позже! 😊")

    @property
    def LIKE_PROFILE(self):
        return _("Кому-то понравилась тваоя анкета! Хочешь посмотреть? 👀")

    @property
    def LIKE_ARCHIVE(self):
        return _("Тебя ещё никто не лайкнул, но всё впереди!")

    @property
    def LIKE_ACCEPT(self):
        return _("Отлично! Надеюсь хорошо проведете время ;) <a href='{}'>{}</a>")

    @property
    def GENDER(self):
        return _("Укажи, свой пол: 👤")

    @property
    def FIND_GENDER(self):
        return _("Выбери, кого ты ищешь: 💕")

    @property
    def PHOTO(self):
        return _("Пришли своё фото! 📸")

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
        return _("Расскажи немного о себе! Это поможет другим лучше тебя узнать. 📝")

    @property
    def DISABLE_PROFILE(self):
        return _(
            "Твоя анкета временно отключена. Чтобы снова её активировать, просто нажми на кнопку. 😊"
        )

    @property
    def ACTIVATE_PROFILE_ALERT(self):
        return _("✅ Твоя анкета успешно восстановлена! Теперь ты снова можешь пользоваться ботом.")

    @property
    def INVALID_RESPONSE(self):
        return _("Некорректный ответ. Пожалуйста, выбери на клавиатуре или напиши правильно. 📝")

    @property
    def INVALID_LONG_RESPONSE(self):
        return _("Превышен лимит символов. Пожалуйста, сократи сообщение. ✂️")

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
            "Приглашай друзей и получай бонусы!\n\nПриглашенные пользователи: <b>{}</b>\n\nСсылка для друзей:\n<code>https://t.me/{}?start={}</code>"
        )

    @property
    def ADMIN_WELCOME(self):
        return _("Ты администратор!")

    @property
    def PROFILE_STATS(self):
        return """
📂 Profile: {} | 🔕 Inactive: {}
🙍‍♂ Guys: {} | 🙍‍♀ Girls: {}

💘 Matchs: {}

🕘 Age: {}
🏙 City: {}
"""

    @property
    def USER_STATS(self):
        return """
👤 Users: {}\t| 🚫 Blocked: {}
✉️ Referrals: {}

🌍 Most popular language: {}
"""

    @property
    def CHANGE_LANG(self):
        return _("Выбери язык бота, на который хочешь переключиться: 🌐")

    @property
    def DONE_CHANGE_LANG(self):
        return _("Язык бот изменён! ✅")

    @property
    def NEW_USER(self):
        return _("Новый пользователь!\n<code>{}</code> (@{})")

    @property
    def REPORT_TO_USER(self):
        return _(
            "Пользователь <code>{}</code> (@{}) отправил жалобу на анкету пользователя: <code>{}</code> (@{})"
        )

    @property
    def USER_PANEL(self):
        return _("Панель управления пользователями:")

    @property
    def UNBAN_USERS_PANEL(self):
        return _(
            "💊 Пожалуйста, укажи список ID пользователей через запятую для разблокировки.\nПример: 1234567, 234567"
        )

    @property
    def BAN_USERS_PANEL(self):
        return _(
            "⚔️ Пожалуйста, укажи список ID пользователей через запятую для блокировки.\nПример: 1234567, 234567"
        )

    @property
    def USER_BANNED(self):
        return _("Пользователь: <code>{}</code> заблокирован")

    @property
    def USER_BANNED_CANCEL(self):
        return _("Администратор отклонил жалобу")

    @property
    def MAILING_PANEL(self):
        return _("Укажи текст сообщения которое будет отправленно")

    @property
    def REPORT_TO_PROFILE(self):
        return _("✅ Жалоба отправлена на рассмотрение!")

    @property
    def RESON_OF_REPORTING(self):
        return _("""Укажи причину жалобы:
🔞 Неприличный материал
💰 Реклама
🔫 Другое

Если жалоба ошибочная, то можете вернутся назад.
""")


msg_text = MsgText()
