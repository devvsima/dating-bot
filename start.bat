@echo off

IF "%1"=="run" (
    uv run main.py
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
