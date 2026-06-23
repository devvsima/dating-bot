#!/bin/bash

case "$1" in
    run)
        uv run main.py
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
        echo "Available commands: run, mapply, mgen, lcollect, lupdate, lcompile"
        ;;
esac
