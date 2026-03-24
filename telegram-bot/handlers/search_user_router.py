from shared.db.database import *
from requests.send import send_data_to_pc
from keyboards.keyboard import *

from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


search_user_router = Router()

## ------ Поиск пользователя --------
class UserSearch(StatesGroup):
    name = State()

@search_user_router.message(F.text == "Поиск пользователя")
async def process_search(message: Message, state: FSMContext):
    # Используем db напрямую, соединение уже открыто благодаря middleware
    await state.set_state(UserSearch.name)
    await message.answer("Введите имя пользователя: ", reply_markup=ReplyKeyboardRemove())

@search_user_router.message(UserSearch.name)
async def process_search(message: Message, state: FSMContext):
    user = await find_user_by_name(message.text)
    
    if user:
        await message.answer(f"Найден: {user['name']}")
    else:
        await message.answer("Не найден", reply_markup=menu_keyboard)

    await state.clear()
## ------ Поиск пользователя --------
