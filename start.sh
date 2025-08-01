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
        uv run pybabel extract --input-dirs=. -o data/locales/bot.pot --project=bot
        ;;
    lupd)
        uv run pybabel update -i data/locales/bot.pot -d data/locales -D bot
        ;;
    lcom)
        uv run pybabel compile -d data/locales -D bot --statistics
        ;;
    *)
        echo "Unknown command: $1"
        echo "Available commands: run, mapply, mgen, lcollect, lupdate, lcompile"
        ;;
esac
