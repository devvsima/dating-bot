@echo off

IF "%1"=="run" (
    uv run main.py
) ELSE IF "%1"=="run_all" (
echo Starting Telegram Bot WebApp...
echo.

echo [1/2] Starting FastAPI WebApp server...
start "WebApp Server" cmd /k python api/run.py

timeout /t 3 /nobreak >nul

echo [2/2] Starting Telegram Bot...
start "Telegram Bot" cmd /k python main.py

echo.
echo Both services are running!
echo - Bot: Running in polling mode
echo.
echo Press any key to exit...
pause >nul
) ELSE IF "%1"=="mapp" (
    uv run alembic upgrade head
) ELSE IF "%1"=="mgen" (
    uv run alembic revision --autogenerate
) ELSE IF "%1"=="lcoll" (
    uv run pybabel extract --input-dirs=. -o data/locales/bot.pot --project=bot
) ELSE IF "%1"=="lupd" (
    uv run pybabel update -i data/locales/bot.pot -d data/locales -D bot
) ELSE IF "%1"=="lcom" (
    uv run pybabel compile -d data/locales -D bot --statistics
) ELSE (
    echo !Unknown command
    echo "Available commands: run, mapply, mgen, lcollect, lupdate, lcompile"
)
