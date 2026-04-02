import aiosqlite
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
DB_PATH = os.getenv("DB_PATH")

## Иницализация БД
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            timestamp DATETIME
        )
    """)
        
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            last_seen DATATIME,
            last_photo TEXT UNIQUE
        )
    """)
        
        await db.commit()
        print("[INFO] База данных инициализирована.")

## Работа с таблицей логов
async def add_log(person):
    name = person["info"]["subject"]
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO logs (name, timestamp) VALUES (?, datetime('now', 'localtime'))", 
            (name,)
        )
        await db.commit()

async def find_log_by_name(name):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT name, timestamp FROM logs WHERE name = ?", (name, )
            )
        person = await cursor.fetchone()
        return dict(person) if person else None
    
## Работа с таблицей пользователей
async def add_user(name):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO users (name) VALUES (?)", 
            (name, )
        )
        await db.commit()

async def update_user_by_name(name, new_photo):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET last_seen = datetime('now', 'localtime'), last_photo = ? WHERE name = ?", (new_photo, name)
        )
        await db.commit()

async def find_user_by_name(name):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM users WHERE name = ?", 
            (name, )
        )
        user = await cursor.fetchone()
        return dict(user) if user else None