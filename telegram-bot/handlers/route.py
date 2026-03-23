import aiosqlite

from shared.db.database import *

from aiogram import F, Router, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

menu_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Добавить пользователя")], 
                               [KeyboardButton(text="Получить последние данные")],
                               [KeyboardButton(text="Поиск пользователя")]], resize_keyboard=True, one_time_keyboard=True)

apply_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отменить"), 
                                                KeyboardButton(text="Подтвердить")]], resize_keyboard=True, one_time_keyboard=True)


router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет, бот работает!", reply_markup=menu_keyboard)


@router.message(Command("close"))
async def close(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Выход выполнен успешно", reply_markup=menu_keyboard)


## ------ Регистрация пользователя --------
class User(StatesGroup):
    name = State()
    photos = State()
    apply = State()


@router.message(F.text == "Добавить пользователя")
async def add_user(message: Message, state: FSMContext):
    await state.set_state(User.name)
    await message.answer('Введите имя пользователя', reply_markup=ReplyKeyboardRemove())

@router.message(User.name)
async def add_user_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(User.photos)
    await message.answer('Отправьте фото пользователя (до 4-х фото)')


@router.message(User.photos, F.photo)
async def add_user_photos(message: Message, state: FSMContext):
    photos = message.photo
    if len(photos) > 4:
        await message.answer('Разрешено отправлять до 4-х фото')
        return
    #
    # Проверка фото через нейросеть
    # 

    await message.answer('Фото пользователя были успешно получены. Добавить пользователя?', reply_markup=apply_keyboard)
    await state.set_state(User.apply)

@router.message(User.apply)
async def add_user_apply(message: Message, state: FSMContext):
    if (message.text == "Подтвердить"):
        ## Запрос в БД
        pass
    elif (message.text == "Отменить"):
        await message.answer("Все действия были отменены", reply_markup=menu_keyboard)
    
    await state.clear()
## ------ Регистрация пользователя --------

## ------ Поиск пользователя --------
class UserSearch(StatesGroup):
    name = State()

@router.message(F.text == "Поиск пользователя")
async def process_search(message: Message, state: FSMContext):
    # Используем db напрямую, соединение уже открыто благодаря middleware
    await state.set_state(UserSearch.name)
    await message.answer("Введите имя пользователя: ", reply_markup=ReplyKeyboardRemove())

@router.message(UserSearch.name)
async def process_search(message: Message, db: aiosqlite.Connection, state: FSMContext):
    user = await find_user_by_name(message.text)
    
    if user:
        await message.answer(f"Найден: {user['name']}")
    else:
        await message.answer("Не найден", reply_markup=menu_keyboard)

    await state.clear()
## ------ Поиск пользователя --------
