from shared.db.database import *
from face_db.face_db import add_subject_face, find_subject, validate_photos
from keyboards.keyboard import *
from handlers.filters.filter import NameLatinitzaFilter

from aiogram import F, Router, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


add_user_router = Router()

## ------ Регистрация пользователя --------
class User(StatesGroup):
    name = State()
    photos = State()
    apply = State()


@add_user_router.message(F.text == "Добавить пользователя")
async def add_user(message: Message, state: FSMContext):
    await state.set_state(User.name)
    await message.answer('Введите имя пользователя', reply_markup=ReplyKeyboardRemove())

# Хендлер для ПРАВИЛЬНОГО имени
@add_user_router.message(User.name, NameLatinitzaFilter())
async def add_user_name(message: Message, state: FSMContext):
    name = message.text
    user_found = await find_subject(name)
    if user_found:
        await state.clear()
        await message.answer(f"❌ Пользователь с именем **{name}** уже зарегистрирован!", reply_markup=menu_keyboard)
    else:
        await state.update_data(name=message.text)
        await state.set_state(User.photos)
        await message.answer('Отправьте фото пользователя (до 4-х фото)')
# Хендлер-ловушка для ОШИБОЧНОГО имени (сработает, если фильтр выше вернул False)
@add_user_router.message(User.name)
async def name_incorrect(message: Message):
    await message.answer(
        "❌ Неверный формат!\n\n"
        "Имя должно состоять из двух слов на латинице (например: Ivan Ivanov)."
    )

@add_user_router.message(User.photos, F.photo)
async def add_user_photos(message: Message, state: FSMContext, bot: Bot, album: list[Message] = None):
    if album:
        new_photo_ids = [msg.photo[-1].file_id for msg in album]
    else:
        new_photo_ids = [message.photo[-1].file_id]

    if len(new_photo_ids) > 4:
        await message.answer('Разрешено отправлять до 4-х фото')
        return
    
    await message.answer("🔍 Проверяю качество и подлинность лиц...")
    
    is_valid, msg, downloaded_photos = await validate_photos(new_photo_ids, bot)
    print(downloaded_photos)

    if not is_valid:
        await message.answer(f"❌ {msg}\nПопробуйте загрузить другие фото.")
    else:
        await state.update_data(photos_ids=new_photo_ids)
        await message.answer('Фото пользователя были успешно получены. Добавить пользователя?', reply_markup=apply_keyboard)
        await state.set_state(User.apply)

@add_user_router.message(User.apply)
async def add_user_apply(message: Message, state: FSMContext, bot: Bot):
    if (message.text == "Подтвердить"):
        data = await state.get_data()
        user_name = data.get("name")
        photos_ids = data.get("photos_ids")
        
        status, responses = await add_subject_face(user_name, photos_ids, bot)
    
        if status == "api_error":
            await message.answer(f"⚠️ Ошибка API: На одном из фото не удалось распознать лицо.", reply_markup=menu_keyboard)
            print(f"Детали ошибки: {responses}")

        elif status == "connection_error":
            await message.answer("🔌 Ошибка соединения: Сервер обработки лиц временно недоступен.", reply_markup=menu_keyboard)

        elif status == "success":
            # Если всё прошло успешно, записываем в нашу локальную БД
            # await save_user_to_db(name) 
            await message.answer(f"✅ Пользователь **{user_name}** успешно добавлен в систему!", reply_markup=menu_keyboard)
        
        else:
            await message.answer(f"🧨 Произошла неизвестная ошибка: {responses}", reply_markup=menu_keyboard)
    
    await state.clear()
## ------ Регистрация пользователя --------