import asyncio
import aiosqlite
import logging
import os

from aiogram import Bot, Dispatcher

from handlers.route import router

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

async def check_new_logs(bot: Bot):
    last_id = 0

    while True:
        try:
            async with aiosqlite.connect("../../../shared_data/security_logs.db") as db:
                async with db.execute("SELECT id, name, timestamp FROM logs WHERE id > ? ORDER BY id DESC LIMIT 1", (last_id)) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        log_id, name, time = row
                        await bot.send_message(YOUR_USER_ID, f"🔔 Внимание! Обнаружен: {name}\nВремя: {time}")
                        last_id = log_id # Обновляем последний виденный ID

        except Exception as e:
            print(f"Ошибка БД: {e}")        

        await asyncio.sleep(1)

async def main():
    dp.include_router(router)
    asyncio.create_task(check_new_logs(bot))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")