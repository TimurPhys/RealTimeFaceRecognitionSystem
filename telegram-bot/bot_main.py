import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import aiosqlite
import logging
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from aiogram import Bot, Dispatcher

from handlers.route import router
from middlewares.db import DBMiddleware

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

DB_PATH = os.getenv("DB_PATH")


async def main():
    dp.include_router(router)
    dp.update.middleware(DBMiddleware(db_path=DB_PATH))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")