from aiogram import Bot, Dispatcher, executor
from app import middlewares, handlers, filters
from loader import dp, bot

async def start_up(_):
    from app.commands import set_default_commands
    await set_default_commands()
    print("< Bot start_up >")   

async def on_shutdown(dispatcher: Dispatcher):
    print("Shutting down...")

if __name__ == "__main__":
    executor.start_polling(
        dp,
        on_startup=start_up,
        on_shutdown=on_shutdown,
        skip_updates=True,
    )
    