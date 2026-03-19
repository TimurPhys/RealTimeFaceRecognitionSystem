import asyncio
import aiosqlite

from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет, бот работает!")