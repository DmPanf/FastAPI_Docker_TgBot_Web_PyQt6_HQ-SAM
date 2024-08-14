# python text_module.py
#

from aiogram import types

# Register All bot commands
commands = [
    types.BotCommand(command="/start", description="♻️ Запустить бота"),
    types.BotCommand(command="/help", description="💡 Показать справку"),
    types.BotCommand(command="/info", description="ℹ️  Информация о проекте"),
    types.BotCommand(command="/models", description="🪩 Доступные Модели"),
    types.BotCommand(command="/id", description="🪪 Получить свой ID"),
    types.BotCommand(command="/list", description="📝 Список разрешенных ID"),
    types.BotCommand(command="/add", description="🛂 Добавить ID в список"),
    types.BotCommand(command="/del", description="🚫 Удалить ID из списка"),
]


help_text = """
*Доступные команды бота:*

/start - ♻️ Начало работы с ботом
/help - 💡 Получить справку по командам
/info - ℹ️  Информация о проекте
/models - 🪩 Доступные Модели
/id - 🪪 Получить свой ID
/list - 📝 Список разрешенных ID
/add - 🛂 Добавить ID в список Администратора
/del - 🚫 Удалить ID из списка

🖼 Отправьте изображение в обработку.
"""

