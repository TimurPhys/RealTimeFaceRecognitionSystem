from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Добавить пользователя")], 
                               [KeyboardButton(text="Получить последние данные")],
                               [KeyboardButton(text="Поиск пользователя")]], resize_keyboard=True, one_time_keyboard=True)

apply_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отменить"), 
                                                KeyboardButton(text="Подтвердить")]], resize_keyboard=True, one_time_keyboard=True)