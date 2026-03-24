from keyboards.keyboard import *

from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext


command_router = Router()

@command_router.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет, бот работает!", reply_markup=menu_keyboard)


@command_router.message(Command("close"))
async def close(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Выход выполнен успешно", reply_markup=menu_keyboard)