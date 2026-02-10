@echo off

IF "%1"=="run" (
    uv run main.py
) ELSE IF "%1"=="api" (
    uv run uvicorn run_api:app --host 0.0.0.0 --port 8080 --reload
) ELSE IF "%1"=="mapp" (
    uv run alembic upgrade head
) ELSE IF "%1"=="mgen" (
    uv run alembic revision --autogenerate
) ELSE IF "%1"=="lcoll" (
    uv run python -m babel.messages.frontend extract -F locales/babel.cfg -o locales/bot.pot .
) ELSE IF "%1"=="lupd" (
    uv run python -m babel.messages.frontend update -i locales/bot.pot -d locales -D bot
) ELSE IF "%1"=="lcom" (
    uv run python -m babel.messages.frontend compile -d locales -D bot --statistics
) ELSE (
    echo !Unknown command
    echo "Available commands: run, api, mapply, mgen, lcollect, lupdate, lcompile"
)
