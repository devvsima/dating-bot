#!/usr/bin/env python3
"""
Простой скрипт для быстрого выполнения полного обновления профилей с геометкой.
Заменяет символ "📍" на названия городов и устанавливает is_shared_location = True.
"""

import asyncio
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.connect import async_session
from database.models.profile import ProfileModel
from utils.geopy import get_city_name
from utils.logging import logger


async def quick_update():
    """Быстрое обновление всех профилей с символом '📍'"""

    print("🚀 Запуск быстрого обновления профилей с геометкой...")
    print("=" * 50)

    async with async_session() as session:
        try:
            # Получаем статистику перед обновлением
            stmt = select(ProfileModel).where(ProfileModel.city.contains("📍"))
            result = await session.execute(stmt)
            profiles = result.scalars().all()

            if not profiles:
                print("✅ Профили с символом '📍' не найдены. Обновление не требуется.")
                return

            print(f"📊 Найдено профилей для обновления: {len(profiles)}")
            print()

            updated_cities = 0
            updated_flags = 0
            failed_geocoding = 0

            for i, profile in enumerate(profiles, 1):
                print(f"🔄 Обрабатываю профиль {i}/{len(profiles)} (ID: {profile.id})")

                try:
                    # Получаем название города
                    city_name = get_city_name(profile.latitude, profile.longitude)

                    old_city = profile.city
                    old_flag = profile.is_shared_location

                    if city_name:
                        profile.city = city_name
                        updated_cities += 1
                        print(f"   ✅ Город: '{old_city}' → '{city_name}'")
                    else:
                        failed_geocoding += 1
                        print(f"   ❌ Не удалось получить название города")

                    # Всегда устанавливаем флаг геолокации
                    if not old_flag:
                        profile.is_shared_location = True
                        updated_flags += 1
                        print(f"   ✅ Флаг геолокации: {old_flag} → True")
                    else:
                        print(f"   ℹ️ Флаг геолокации уже установлен")

                except Exception as e:
                    print(f"   ❌ Ошибка: {e}")
                    failed_geocoding += 1

                print()

            # Сохраняем изменения
            print("💾 Сохранение изменений в базе данных...")
            await session.commit()

            # Выводим итоги
            print("=" * 50)
            print("🎉 ОБНОВЛЕНИЕ ЗАВЕРШЕНО!")
            print(f"📊 Итоги:")
            print(f"   • Всего обработано профилей: {len(profiles)}")
            print(f"   • Успешно обновлено городов: {updated_cities}")
            print(f"   • Установлено флагов геолокации: {updated_flags}")
            if failed_geocoding > 0:
                print(f"   • Ошибок геокодирования: {failed_geocoding}")

            logger.log(
                "SCRIPT",
                f"Быстрое обновление завершено: {updated_cities} городов, "
                f"{updated_flags} флагов, {failed_geocoding} ошибок",
            )

        except Exception as e:
            await session.rollback()
            print(f"❌ Критическая ошибка: {e}")
            logger.error(f"Критическая ошибка при быстром обновлении: {e}")
            raise


async def show_preview():
    """Показывает что будет обновлено"""

    print("👀 ПРЕДВАРИТЕЛЬНЫЙ ПРОСМОТР")
    print("=" * 50)

    async with async_session() as session:
        try:
            stmt = select(ProfileModel).where(ProfileModel.city.contains("📍"))
            result = await session.execute(stmt)
            profiles = result.scalars().all()

            if not profiles:
                print("✅ Профили с символом '📍' не найдены.")
                return

            print(f"📊 Будет обработано профилей: {len(profiles)}\n")

            will_update_cities = 0
            will_update_flags = 0

            for i, profile in enumerate(profiles, 1):
                print(f"{i}. Профиль ID: {profile.id}")
                print(f"   Текущий город: '{profile.city}'")
                print(f"   Координаты: ({profile.latitude}, {profile.longitude})")
                print(f"   Флаг геолокации: {profile.is_shared_location}")

                try:
                    city_name = get_city_name(profile.latitude, profile.longitude)
                    if city_name:
                        print(f"   ✅ Новый город: '{city_name}'")
                        will_update_cities += 1
                    else:
                        print(f"   ❌ Город не определился")
                except Exception as e:
                    print(f"   ❌ Ошибка: {e}")

                if not profile.is_shared_location:
                    print(f"   ✅ Флаг геолокации будет установлен в True")
                    will_update_flags += 1
                else:
                    print(f"   ℹ️ Флаг геолокации уже установлен")

                print()

            print("=" * 50)
            print(f"📊 ИТОГО БУДЕТ ОБНОВЛЕНО:")
            print(f"   • Городов: {will_update_cities}")
            print(f"   • Флагов геолокации: {will_update_flags}")

        except Exception as e:
            print(f"❌ Ошибка при предварительном просмотре: {e}")
            raise


def print_help():
    """Справка по использованию"""
    print("""
🚀 БЫСТРОЕ ОБНОВЛЕНИЕ ПРОФИЛЕЙ С ГЕОМЕТКОЙ

Использование: python quick_update_profiles.py [команда]

Команды:
    run        - Выполнить полное обновление (город + флаг геолокации)
    preview    - Предварительный просмотр изменений
    help       - Показать эту справку

Примеры:
    python quick_update_profiles.py preview
    python quick_update_profiles.py run

Что делает скрипт:
    1. Находит все профили с символом "📍" в поле city
    2. Заменяет символ на реальное название города (через геокодирование)
    3. Устанавливает флаг is_shared_location = True
    4. Сохраняет изменения в базе данных

⚠️ ВНИМАНИЕ: Команда 'run' сразу выполняет изменения без дополнительных запросов!
Используйте 'preview' для предварительного просмотра.
    """)


async def main():
    """Главная функция"""

    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()

    if command == "preview":
        await show_preview()

    elif command == "run":
        await quick_update()

    elif command == "help":
        print_help()

    else:
        print(f"❌ Неизвестная команда: {command}")
        print("\nИспользуйте 'help' для просмотра доступных команд.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Операция прервана пользователем.")
    except Exception as e:
        print(f"💥 Критическая ошибка: {e}")
        sys.exit(1)
