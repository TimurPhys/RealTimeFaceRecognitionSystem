import aiosqlite
import cv2
import numpy as np

DB_PATH = "./shared_data/security_system.db"

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
            last_photo BLOB
        )
    """)
        
        await db.commit()
        print("[INFO] База данных инициализирована.")

async def add_log(person):
    name = person["info"]["subject"]
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO logs (name, timestamp) VALUES (?, datetime('now', 'localtime'))", 
            (name,)
        )
        await db.commit()