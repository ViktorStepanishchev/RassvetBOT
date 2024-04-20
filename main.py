import asyncio
from aiogram import Bot, Dispatcher
from routers.handlers import router_handlers
from routers.registration import router_registration
from routers.edit_anketa import router_edit

from base import create_db

async def main():
    bot = Bot(token=open("token").readline(), parse_mode="HTML")

    dp = Dispatcher()
    create_db()
    dp.include_routers(router_handlers, router_registration, router_edit)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    loop.create_task(main())

    loop.run_forever()