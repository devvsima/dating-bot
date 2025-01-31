from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def simple_kb_generator(*buttons_list: list, one_time: bool = True, resize: bool = True) -> ReplyKeyboardMarkup:
    """
    Небольшой генератор клавиатуры.
    !Не желатьельно использовать с текстом который требует перевода.
    
    :param buttons: строки с названиями кнопок (будут располагаться в одном ряду)
    :param one_time: скрывать ли клавиатуру после нажатия (по умолчанию True)
    :param resize: уменьшать ли клавиатуру (по умолчанию True)
    :return: объект ReplyKeyboardMarkup
    """
    keyboard = []
    for buttons in buttons_list:
        kb = []
        for btn_text in buttons:
            kb += [KeyboardButton(text=btn_text)]
        keyboard.append(kb)
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=resize,
        one_time_keyboard=one_time
    )
