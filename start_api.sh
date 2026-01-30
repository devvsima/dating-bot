#!/bin/bash
# Скрипт для запуска API сервера на production сервере

# Установите переменные окружения или создайте .env файл
export HOST="0.0.0.0"
export PORT="8080"

# Запуск через uvicorn с несколькими воркерами
uvicorn webapp:app \
    --host $HOST \
    --port $PORT \
    --workers 4 \
    --log-level info \
    --proxy-headers \
    --forwarded-allow-ips '*'
