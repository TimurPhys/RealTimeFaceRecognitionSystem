import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import logging
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from aiogram import Bot, Dispatcher

from handlers.add_user_router import add_user_router
from handlers.command_router import command_router
from handlers.search_user_router import search_user_router

from middlewares.db import DBMiddleware
from middlewares.album import AlbumMiddleware

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

DB_PATH = os.getenv("DB_PATH")


async def main():
    dp.include_router(add_user_router)
    dp.include_router(command_router)
    dp.include_router(search_user_router)
    dp.message.middleware(DBMiddleware(db_path=DB_PATH))
    dp.message.middleware(AlbumMiddleware(0.5))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")