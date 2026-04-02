from aiogram import Bot
from aiogram.types import BotCommand

main_menu_commands = {
        "start": BotCommand(command='/start', description='Запустить бота'),
        "leave": BotCommand(command='/leave', description='Выйти'),
    }

async def set_main_menu(bot: Bot):
    # Список команд, которые увидит пользователь
    await bot.set_my_commands(main_menu_commands.values())
    print("Команды установлены")

async def add_command(command_name, description, bot: Bot):
    main_menu_commands[command_name] = BotCommand(command=f"/{command_name}", description=description)
    await set_main_menu(bot)

async def remove_command(command_name, bot: Bot):
    main_menu_commands.pop(command_name)
    await set_main_menu(bot)