# Инструкция по запуску API на сервере

## 📋 Что изменилось

1. **Убран WebApp интерфейс** - теперь только API
2. **Добавлена защита** - проверка подписи Telegram WebApp через middleware
3. **Добавлен CORS** - для работы с внешним фронтендом
4. **Конфигурация для production** - готовые скрипты запуска

## 🔐 Как работает защита

API защищен проверкой подписи Telegram WebApp. Каждый запрос должен содержать заголовок:

```
Authorization: tma <initData>
```

Где `initData` - это данные от Telegram WebApp (строка вида `query_id=...&user=...&hash=...`)

### Пример запроса с фронтенда:

```javascript
const tg = window.Telegram.WebApp;
const initData = tg.initData; // Telegram автоматически заполняет это

fetch("https://your-api.com/api/profile/123456", {
  headers: {
    Authorization: `tma ${initData}`,
  },
});
```

## 🚀 Запуск на сервере

### Вариант 1: Uvicorn (простой, рекомендуется)

```bash
# Установите зависимости (выберите один вариант)

# Если используете pip:
pip install uvicorn[standard]

# Если используете uv:
uv pip install uvicorn[standard]

# Запустите сервер (выберите один вариант)

# Прямой запуск:
uvicorn webapp:app --host 0.0.0.0 --port 8080 --workers 4

# Через uv (если установили через uv):
uv run uvicorn webapp:app --host 0.0.0.0 --port 8080 --workers 4
```

Или используйте готовый скрипт:

```bash
chmod +x start_api.sh
./start_api.sh
```

### Вариант 2: Gunicorn + Uvicorn workers (рекомендуется для production)

```bash
# Установите зависимости (выберите один вариант)

# Если используете pip:
pip install gunicorn uvicorn[standard]

# Если используете uv:
uv pip install gunicorn uvicorn[standard]

# Запустите с конфигурацией
gunicorn -c gunicorn_config.py webapp:app

# Или через uv (если установили через uv):
uv run gunicorn -c gunicorn_config.py webapp:app
```

### Вариант 3: Systemd service (автозапуск)

1. Скопируйте файл `api.service` в `/etc/systemd/system/`:

```bash
sudo cp api.service /etc/systemd/system/dating-bot-api.service
```

2. Отредактируйте пути в файле:

```bash
sudo nano /etc/systemd/system/dating-bot-api.service
```

3. Включите и запустите сервис:

```bash
sudo systemctl daemon-reload
sudo systemctl enable dating-bot-api
sudo systemctl start dating-bot-api
sudo systemctl status dating-bot-api
```

4. Просмотр логов:

```bash
sudo journalctl -u dating-bot-api -f
```

## 🌐 Nginx конфигурация (опционально)

Если используете Nginx как reverse proxy:

```nginx
server {
    listen 80;
    server_name your-api-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Для HTTPS добавьте SSL сертификат (Let's Encrypt):

```bash
sudo certbot --nginx -d your-api-domain.com
```

## ⚙️ Настройка CORS

В файле `webapp.py` измените настройки CORS для production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],  # Укажите домен фронтенда
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

## 📝 Переменные окружения

Убедитесь что в `.env` файле указаны:

```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_here

# API Server
WEBAPP_HOST=0.0.0.0
WEBAPP_PORT=8080
WEBAPP_DOMEN=your-api-domain.com
WEBAPP_URL=https://your-api-domain.com

# API Access Token для тестирования (опционально)
# Генерируйте случайную строку: openssl rand -hex 32
API_ACCESS_TOKEN=your_secret_access_token_for_testing

# Database
DB_NAME=your_db
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=your_password
```

## 🔑 Два способа аутентификации

API поддерживает два типа авторизации:

### 1. Telegram WebApp (для production)
```javascript
const tg = window.Telegram.WebApp;

fetch('https://your-api.com/api/profile/123456', {
    headers: {
        'Authorization': `tma ${tg.initData}`
    }
})
```

### 2. Bearer Token (для тестирования)
```bash
# Сгенерируйте токен
openssl rand -hex 32

# Добавьте в .env
API_ACCESS_TOKEN=ваш_токен

# Используйте в запросах
curl http://localhost:8080/api/profile/123456 \
  -H "Authorization: Bearer ваш_токен"
```

Пример с Postman/Insomnia:
```
Authorization: Bearer ваш_токен
```

Пример с JavaScript:
```javascript
fetch('https://your-api.com/api/profile/123456', {
    headers: {
        'Authorization': 'Bearer ваш_токен'
    }
})
```

## 🧪 Тестирование API

### Проверка работы сервера:

```bash
curl http://localhost:8080/
```

Ответ:

```json
{
  "name": "Dating Bot API",
  "version": "1.0.0",
  "status": "running"
}
```

### Документация API:

Откройте в браузере:

- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

## 📦 Зависимости

Убедитесь что установлены все необходимые пакеты:

```bash
pip install fastapi uvicorn[standard] gunicorn python-multipart
```

## 🔧 Полезные команды

```bash
# Остановить сервис
sudo systemctl stop dating-bot-api

# Перезапустить сервис
sudo systemctl restart dating-bot-api

# Проверить статус
sudo systemctl status dating-bot-api

# Посмотреть логи
sudo journalctl -u dating-bot-api -f

# Проверить ошибки конфигурации
gunicorn -c gunicorn_config.py webapp:app --check-config
```

## 🐛 Решение проблем

### API не запускается

- Проверьте логи: `sudo journalctl -u dating-bot-api -f`
- Убедитесь что порт 8080 не занят: `sudo lsof -i :8080`
- Проверьте права доступа к файлам

### Ошибка подключения к базе данных

- Проверьте что PostgreSQL запущен: `sudo systemctl status postgresql`
- Проверьте настройки подключения в `.env`

### CORS ошибки

- Убедитесь что в `webapp.py` указан правильный домен фронтенда
- Проверьте что фронтенд отправляет правильный заголовок `Authorization`

### 401 Unauthorized

- **Telegram WebApp:** Проверьте что фронтенд отправляет `Authorization: tma <initData>`
- **Bearer Token:** Проверьте что токен в заголовке совпадает с `API_ACCESS_TOKEN` в `.env`
- Убедитесь что `TELEGRAM_BOT_TOKEN` в `.env` совпадает с токеном бота

## 📞 Дополнительная информация

- Документация Telegram WebApp: https://core.telegram.org/bots/webapps
- Документация FastAPI: https://fastapi.tiangolo.com/
- Документация Uvicorn: https://www.uvicorn.org/
