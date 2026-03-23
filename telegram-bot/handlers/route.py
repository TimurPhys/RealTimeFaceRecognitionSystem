import asyncio
import aiosqlite

from aiogram import F, Router, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

menu_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Добавить пользователя")], 
                               [KeyboardButton(text="Получить последние данные")],
                               [KeyboardButton(text="Поиск пользователя")]], resize_keyboard=True, one_time_keyboard=True)

apply_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отменить"), KeyboardButton(text="Подтвердить")]], resize_keyboard=True, one_time_keyboard=True)

class User(StatesGroup):
    name = State()
    photos = State()
    apply = State()

router = Router()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет, бот работает!", reply_markup=menu_keyboard)

@router.message(F.text == "Добавить пользователя")
async def add_user(message: Message, state: FSMContext):
    await state.set_state(User.name)
    await message.answer('Введите имя пользователя')

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
    pass
    