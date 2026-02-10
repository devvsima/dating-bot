#!/bin/bash

case "$1" in
    run)
        uv run main.py
        ;;
    api)
        uv run uvicorn run_api:app --host 0.0.0.0 --port 8080 --workers 4 --log-level info
        ;;
    mapp)
        uv run alembic upgrade head
        ;;
    mgen)
        uv run alembic revision --autogenerate
        ;;
    lcoll)
        uv run python -m babel.messages.frontend extract -F locales/babel.cfg -o locales/bot.pot .
        ;;
    lupd)
        uv run python -m babel.messages.frontend update -i locales/bot.pot -d locales -D bot
        ;;
    lcom)
        uv run python -m babel.messages.frontend compile -d locales -D bot --statistics
        ;;
    *)
        echo "Unknown command: $1"
        echo "Available commands: run, api, mapply, mgen, lcollect, lupdate, lcompile"
        ;;
esac
