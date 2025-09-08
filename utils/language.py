"""
Утилиты для работы с языками и локализацией
"""

def get_supported_language(language_code: str) -> str:
    """
    Возвращает поддерживаемый язык на основе кода языка пользователя.
    Если язык не поддерживается, возвращает английский по умолчанию.
    
    Args:
        language_code: Код языка пользователя (например, 'ru', 'en', 'de')
        
    Returns:
        str: Поддерживаемый код языка
    """
    if language_code and language_code in SUPPORTED_LOCALES:
        return language_code
    
    # Если язык не поддерживается, возвращаем английский по умолчанию
    return DEFAULT_LOCALE


# Константы для использования в других модулях
SUPPORTED_LOCALES = ["en", "ru", "uk", "fr", "pl", "es", "id"]  # Добавлен индонезийский
DEFAULT_LOCALE = "en"
