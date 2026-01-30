"""
FastAPI API server для Telegram Dating Bot
Защищен проверкой подписи Telegram WebApp
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import api_router
from api.middleware import TelegramWebAppMiddleware
from data.config import tgbot, webapp
from utils.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events - события жизненного цикла приложения"""
    logger.log("API", "~ API server started")
    yield
    logger.log("API", "~ API server shutting down...")


app = FastAPI(
    title="Dating Bot API",
    description="Protected API for Telegram Dating Bot WebApp",
    version="1.0.0",
    lifespan=lifespan,
)

# Настройка CORS для внешнего фронтенда
# ВАЖНО: В production укажите конкретные домены вместо "*"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В production замените на ["https://your-frontend.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем middleware для проверки Telegram WebApp подписи
app.add_middleware(
    TelegramWebAppMiddleware,
    bot_token=tgbot.BOT_TOKEN,
    access_token=webapp.ACCESS_TOKEN,
)

# Подключаем API роутеры
app.include_router(api_router)


@app.get("/")
async def root():
    """Корневой endpoint - информация об API"""
    return {
        "name": "Dating Bot API",
        "version": "1.0.0",
        "status": "running",
        "description": "Protected API with Telegram WebApp signature validation",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "webapp:app",
        host=webapp.HOST,
        port=webapp.PORT,
        reload=True,
    )
