"""
FastAPI server для Telegram WebApp
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api import api_router
from data.config import webapp
from utils.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events - события жизненного цикла приложения"""
    logger.log("WEBAPP", "~ WebApp server started")
    yield
    logger.log("WEBAPP", "~ WebApp server shutting down...")


app = FastAPI(title="Telegram WebApp", lifespan=lifespan)

# Подключаем API роутеры
app.include_router(api_router)

# Подключаем статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")
templates = Jinja2Templates(directory="webapp/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Главная страница webapp"""
    response = templates.TemplateResponse("index.html", {"request": request})
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("webapp_server:app", host=webapp.HOST, port=webapp.PORT, reload=True)
