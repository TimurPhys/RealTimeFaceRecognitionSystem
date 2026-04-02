from ..keyboards.keyboard import *
from ..keyboards.menu import *

from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

command_router = Router()

@command_router.message(CommandStart())
async def start(message: Message, bot: Bot):
    await message.answer("Привет, бот работает!", reply_markup=menu_keyboard)
    await set_main_menu(bot)


@command_router.message(Command("leave"))
async def close(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Выход выполнен успешно", reply_markup=menu_keyboard)