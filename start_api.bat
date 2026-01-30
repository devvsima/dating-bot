@echo off
REM Скрипт для запуска API сервера на Windows

REM Установите переменные окружения или создайте .env файл
set HOST=0.0.0.0
set PORT=8080

REM Запуск через uvicorn
uvicorn webapp:app --host %HOST% --port %PORT% --reload
