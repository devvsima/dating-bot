"""
Gunicorn конфигурация для production запуска API сервера
"""

import multiprocessing

# Адрес и порт
bind = "0.0.0.0:8080"

# Количество worker процессов
# Рекомендуется: (2 * CPU_cores) + 1
workers = multiprocessing.cpu_count() * 2 + 1

# Класс worker процессов (uvicorn для async)
worker_class = "uvicorn.workers.UvicornWorker"

# Таймауты
timeout = 120
keepalive = 5

# Логирование
accesslog = "logs/api_access.log"
errorlog = "logs/api_error.log"
loglevel = "info"

# Перезапуск worker при утечке памяти
max_requests = 1000
max_requests_jitter = 50

# Graceful timeout
graceful_timeout = 30

# Preload приложения для экономии памяти
preload_app = True
