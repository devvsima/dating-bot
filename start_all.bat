@echo off
echo Starting Telegram Bot WebApp...
echo.

echo [1/2] Starting FastAPI WebApp server...
start "WebApp Server" cmd /k python webapp_server.py

timeout /t 3 /nobreak >nul

echo [2/2] Starting Telegram Bot...
start "Telegram Bot" cmd /k python main.py

echo.
echo Both services are running!
echo - Bot: Running in polling mode
echo.
echo Press any key to exit...
pause >nul
