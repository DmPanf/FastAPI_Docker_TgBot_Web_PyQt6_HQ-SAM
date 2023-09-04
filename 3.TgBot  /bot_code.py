from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import requests
import asyncio
import aiohttp
import json
from dotenv import load_dotenv
from io import BytesIO
from datetime import datetime
from PIL import Image
import os

# Load environment variables
load_dotenv()
API_TOKEN = os.getenv("TOKEN")
ADMIN_CHAT_ID = os.getenv("CHAT_ID")
API_URL = 'http://api-serv.ru:8001/models'

if not API_TOKEN:
    raise ValueError("TG_TOKEN is not set in the environment variables or .env file!")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def on_startup(dp):
    bot_info = await dp.bot.get_me()
    bot_name = bot_info.username
    await dp.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f'✴️ Бот @{bot_name} запущен!')
    print(f'✴️  Бот {bot_name} запущен!')

    # Register bot commands
    commands = [
        types.BotCommand(command="/start", description="♻️ Запустить бота"),
        types.BotCommand(command="/help", description="💡 Показать справку"),
        types.BotCommand(command="/info", description="ℹ️  Информация о проекте"),
        types.BotCommand(command="/id", description="🪪 Получить свой ID"),
        types.BotCommand(command="/list", description="📝 Список разрешенных ID"),
        types.BotCommand(command="/add", description="🛂 Добавить ID в список"),
    ]

    await dp.bot.set_my_commands(commands)


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

@dp.message_handler(commands=['start'])
async def send_info(message: types.Message):
    async with aiohttp.ClientSession() as session:
        info = await fetch(session, API_URL)
        await message.answer(f"Project Info:\n{info}")


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    help_text = """
*Доступные команды бота:*

/start - Начало работы с ботом
/help - Получить справку по командам
/info - Информация о проекте
/id - Получить свой ID
/list - Список разрешенных ID
/add - Добавить ID в список Администратора

🖼 Отправьте изображение в обработку.
"""

    await message.reply(help_text, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['models'])
async def send_models(message: types.Message):
    # Инициализация асинхронной сессии HTTP
    async with aiohttp.ClientSession() as session:
        # Загрузка списка моделей с помощью функции fetch(), которая выполняет GET-запрос.
        # API_URL должна быть предварительно определена или передана как аргумент.
        models_list = json.loads(await fetch(session, API_URL))

        # Создание разметки для inline-кнопок
        markup = InlineKeyboardMarkup()

        # Предполагается, что 'Models' в ответе API — это уже список имен моделей
        for model in models_list['Models']:
            # Добавление кнопки для каждой модели. При нажатии будет отправлен callback_data со значением model
            markup.add(InlineKeyboardButton(model, callback_data=model))

        # Отправка сообщения с inline-кнопками
        await message.answer("Choose a model:", reply_markup=markup)


# handler for receiving images and making POST requests to FastAPI
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def process_image(message: types.Message):
    # Получение файла изображения
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    # Загрузка изображения
    image_data = await bot.download_file(file_path)

    # Отправка изображения на сервер
    url = API_URL + 'predict'
    response = requests.post(url, files={"image": ("input_image.png", image_data, "image/png")})

    if response.status_code == 200:
        # Получение обработанного изображения и отправка его обратно пользователю
        output_image_data = BytesIO(response.content)
        output_image_data.seek(0)
        await message.reply_photo(photo=output_image_data, caption="Обработанное изображение")


async def main():
    await on_startup(dp)
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
