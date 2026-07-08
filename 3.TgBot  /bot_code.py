# python bot_code.py
# v1.2

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler  # Импортируйте CancelHandler
import logging
import requests
import asyncio
import aiohttp
from aiohttp import ClientSession, ClientTimeout
import json
from dotenv import load_dotenv
from io import BytesIO
from datetime import datetime
from PIL import Image
import os
from tools import load_servers_list, update_env_variable
from text_module import commands, help_text

# Load environment variables
load_dotenv()
API_TOKEN = os.getenv("TOKEN")
ADMIN_CHAT_ID = os.getenv("CHAT_ID")
#ACCESS_LIST = os.getenv("ACCESS_LIST")
#ACCESS_LIST = list(map(int, os.getenv("ACCESS_LIST", "").split(",")))
ACCESS_LIST = list(map(int, os.getenv("ACCESS_LIST").split(",")))
blocked_users = set()  # глобальный set для хранения ID заблокированных пользователей и возможного получения телефона

# print(f'... ACCESS_LIST: {ACCESS_LIST}')
log_folder = os.getenv("LOG_DIR")
log_file = os.getenv("LOG_FILE")

  
if not API_TOKEN:
    raise ValueError("TG_TOKEN is not set in the environment variables or .env file!")
if not os.path.exists(log_folder):  # Создание директории для логов, если её нет
    os.makedirs(log_folder)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"{log_folder}/{log_file}"),
        logging.StreamHandler()
    ]
)


class AccessMiddleware(BaseMiddleware):  # БЛОКИРОВКА ПОЛЬЗОВАТЕЛЕЙ НА ЛЮБЫЕ ДЕЙСТВИЯ С БОТОМ!!!
    def __init__(self, access_list):
        self.access_list = access_list
        super().__init__()
        #super(AccessMiddleware, self).__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        logging.info(f"msg from: {user_id} ({message.from_user.full_name})")
        # print(f' ----- {user_id}: {self.access_list}')
       
        if user_id not in self.access_list:
            add_text = f"Уважаемый, <b>{message.from_user.full_name}</b> [<code>{message.from_user.username}</code>]!\n"
            add_text += f"Бот находится в разработке!\nДоступ с вашего <b>ID</b> [<code>{user_id}</code>] ограничен!"
            # add_text += "\nПожалуйста, отправьте свой номер телефона для регистрации:"
            await message.answer(f"{add_text}", parse_mode="HTML")
            blocked_users.add(user_id)  # добавляем ID заблокированных пользователей в set
            update_env_variable("BLOKED_LIST", ','.join(map(str, blocked_users)))
            print(f'... blocked_users: {blocked_users}')
            raise CancelHandler()  # Остановить дальнейшую обработку для "настойчивого" пользователя
            #return True  # True означает, что дальнейшая обработка сообщения не требуется
        return False  # Для остальных случаев пропускаем сообщение для дальнейшей обработки 

# logging.basicConfig(level=logging.DEBUG)  # Устанавливаем уровень логирования DEBUG !!!
# logging.basicConfig(level=logging.INFO)  # Устанавливаем уровень логирования INFO
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(ACCESS_LIST))

# API_URL = 'http://api-serv.ru:8001'
# API_URL = 'http://X.X.X.X:33021'
# API_URL = os.getenv("API_URL")
servers_list = load_servers_list(bot)


async def on_startup(dp):
    bot_info = await dp.bot.get_me()
    bot_name = bot_info.username
    user_id = bot_info.id
    await dp.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f'✴️ Бот @{bot_name} запущен!\n🈳 Server: hpai')
    print(f'✴️  Бот {bot_name} запущен!')
    if user_id not in ACCESS_LIST:
        await dp.bot.set_my_commands(commands)


async def fetch(session, url):
    """
    import aiohttp  # Импорт библиотеки aiohttp для асинхронного HTTP-клиента
    Функция для выполнения асинхронного GET-запроса.
    Здесь используется асинхронный HTTP-клиент aiohttp для выполнения GET-запроса.
    Функция fetch принимает в качестве аргументов экземпляр aiohttp.ClientSession и URL. 
    Затем она выполняет GET-запрос к данному URL и возвращает текстовый ответ.

    Параметры:
    - session (aiohttp.ClientSession): экземпляр сессии для асинхронных HTTP-запросов
    - url (str): URL, на который нужно выполнить GET-запрос
    Возвращает:
    - str: текстовый ответ от сервера
    """
    async with session.get(url) as response:  # Использование асинхронного менеджера контекста для выполнения GET-запроса
        return await response.text()          # Возврат текстового содержимого ответа


@dp.message_handler(commands=['start','info'])
async def send_info(message: types.Message):
    API_URL = os.getenv("API_URL")  #  получаем значение переменной из .env файла
    print(f' ... API_URL/info: {API_URL}')
    timeout = ClientTimeout(total=5)  # Устанавливаем общий таймаут в 5 секунд
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            info = await fetch(session, f'{API_URL}/info') 
            data = json.loads(info)["Project 2023"]
            await message.answer(f"🔰 <b>Project Info:</b>\n<pre>{data}</pre>", parse_mode="HTML", reply_markup=keyboard)
        except Exception as e:
            print(f"info ------ Error occurred: {e}")
            await message.answer(f"⛔️ Сервер <b>FastAPI</b> недоступен!\n{e}", parse_mode="HTML", reply_markup=keyboard)


    
# ++++++++++++++++++++ Main KeyBoard ++++++++++++++++
# Создаем обычные кнопки
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row(KeyboardButton('📡Server'), KeyboardButton('⚖️Model'), KeyboardButton('🪬INFO'), KeyboardButton('💡HELP'))

# Обработка текстовых сообщений
@dp.message_handler(lambda message: message.text == '⚖️Model')
async def handle_model(message: types.Message):
    await send_models(message)

@dp.message_handler(lambda message: message.text == '🪬INFO')
async def handle_info(message: types.Message):
    await send_info(message)

@dp.message_handler(lambda message: message.text == '💡HELP')
async def handle_help(message: types.Message):
    #await send_help(message)
    await message.reply(help_text, parse_mode="Markdown")


# ++++++++++++ SERVERS +++++++++++++++++
@dp.message_handler(lambda message: message.text == '📡Server')
async def choose_server(message: types.Message):
    API_URL = os.getenv("API_URL")  #  получаем значение переменной из .env файла 

    markup = InlineKeyboardMarkup()  # Создаем inline-кнопки для серверов
    if servers_list:  # проверяем, есть ли в списке серверов сервер текущего пользователя 
        for server in servers_list:
            server_name = server['name']
            server_url = server['url']
            prefix = "🟩 " if server_url == API_URL else "⬜️ "
            markup.add(InlineKeyboardButton(f"{prefix}{server_name}", callback_data=f"server_{server_url}"))

        update_env_variable("API_URL", API_URL)  # сохраняем выбранный сервер в .env файл !!!
        print(f' ......... Server: {API_URL}')
        current_time = datetime.now().strftime("%H:%M:%S")
        msg = f"📡 Выбор сервера...\nТекущее время: <b>[{current_time}</b>]"
        await message.answer(msg, parse_mode="HTML", reply_markup=markup)
    else:
        await message.answer("⭕️ Список серверов <b>пуст</b>.", parse_mode="HTML")


@dp.callback_query_handler(lambda call: call.data.startswith("server_"))  # !! необходимы фильтры для различия между двумя типами callback_data !!
async def servers_callback_inline(call: CallbackQuery):
    API_URL = os.getenv("API_URL")  #  получаем значение переменной из .env файла 
    current_time = datetime.now().strftime("%H:%M:%S")
    if call.data.startswith("server_"):
        server_url = call.data[7:]
        server_name = [s['name'] for s in servers_list if s['url'] == server_url]
        if server_url == API_URL:
            await call.answer(f"[{current_time}] Сервер {server_name} уже выбран")
        else:
            await change_server(call, server_url)


async def change_server(call: CallbackQuery, new_server_url: str):
    API_URL = new_server_url
    update_env_variable("API_URL", API_URL)  # сохраняем выбранный сервер в .env файл !!!
    print(f' ..... New Server: {API_URL}')

    current_time = datetime.now().strftime("%H:%M:%S")
    msg = f'📡 Выбор сервера...\nТекущее время: <b>{current_time}</b>'
    
    markup = InlineKeyboardMarkup()
    for server in servers_list:
        prefix = "🟩 " if server['url'] == API_URL else "⬜️ "
        markup.add(InlineKeyboardButton(f"{prefix}{server['name']}", callback_data=f"server_{server['url']}"))
        
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text = msg,
        reply_markup=markup,
        parse_mode="HTML"
    )
    await call.answer(f"🟩 Сервер {new_server_url} выбран!")


# ++++++++++ MODELS ++++++++++++++
@dp.message_handler(commands=['models'])
async def send_models(message: types.Message):
    API_URL = os.getenv("API_URL")  #  получаем значение переменной API_URL из .env файла
    BEST_MODEL = os.getenv("mdl_name")  #  получаем значение переменной mdl_name из .env файла
    # models_list = os.getenv("models_list")  #  получаем список моделей из .env файла
    timeout = ClientTimeout(total=10)  # Устанавливаем общий таймаут в 10 секунд

    async with aiohttp.ClientSession(timeout=timeout) as session:  # Инициализация асинхронной сессии HTTP
        try:
            #print(f'1. ... API_URL/models: {API_URL}/models')
            Models = json.loads(await fetch(session, f'{API_URL}/models'))  # Загрузка списка моделей
            #print(f'2. ... Models: {Models}')
            models_list = Models['Models']
            markup = InlineKeyboardMarkup()  # Создание разметки для inline-кнопок
            #print(f"3. ===> models_list: {models_list}")
            
            if models_list:
                if BEST_MODEL in models_list:
                    mdl_name = BEST_MODEL
                    #print(f'4a. .... Best Model: {mdl_name}')
                else:
                    mdl_name = models_list[-1]
                    #print(f'4b. .... Best Model: {mdl_name}')
                
                for model in models_list:  # Добавление inline-кнопок с моделями в разметку
                    prefix = "🟢 " if model == mdl_name else "⚪️ "
                    markup.add(InlineKeyboardButton(f"{prefix}{model}", callback_data=model))  # Добавление кнопки: при нажатии будет отправлен callback_data со значением model
                
                update_env_variable("mdl_name", mdl_name)  # сохраняем выбранную модель mdl_name в .env файл !!!
                # update_env_variable("models_list", models_list)  # сохраняем список моделей models_list в .env файл !!!
                update_env_variable("models_list", ','.join(models_list))  # сохраняем список моделей models_list в .env файл !!!
                #print(f"5. ......... Models: {','.join(models_list)}")
                current_time = datetime.now().strftime("%H:%M:%S")
                msg = f"🪩 Выбор нейромодели...\nТекущее время: <b>[{current_time}</b>]"
                await message.answer(msg, parse_mode="HTML", reply_markup=markup)  # Отправка сообщения с inline-кнопками

            else:
                await message.answer("⭕️ Список моделей <b>пуст</b>.", parse_mode="HTML")
        except Exception as e:
            await message.answer("⛔ Невозможно загрузить список моделей. Проверьте соединение с сервером.\n{e}")


@dp.callback_query_handler(lambda call: not call.data.startswith("server_"))   # !! необходимы фильтры для различия между двумя типами callback_data !!
async def models_callback_inline(call: CallbackQuery):
    BEST_MODEL = os.getenv("mdl_name")  #  получаем значение переменной mdl_name из .env файла
    current_time = datetime.now().strftime("%H:%M:%S")
    if call.data == BEST_MODEL:
        await call.answer(f"[{current_time}] Модель {BEST_MODEL} уже выбрана!")
    else:
        print(type(call.data), call.data)
        await change_model(call, call.data)


async def change_model(call: CallbackQuery, new_model: str):
    mdl_name = new_model
    #print(f'X1 ..... New Model: {mdl_name}')
    update_env_variable("mdl_name", mdl_name)  # сохраняем выбранную модель mdl_name в .env файл !!!
    models_list = os.getenv("models_list").split(',')  #  получаем список моделей из .env файла 
    print(f' ......... New Model: {mdl_name}')
    #print(f' ....... models_list: {models_list}')

    current_time = datetime.now().strftime("%H:%M:%S")
    msg = f'🪩 Выбор нейромодели...\nТекущее время: <b>{current_time}</b>'
    
    markup = InlineKeyboardMarkup()
    #for model in models_list['Models']:  # Старая версия (при получении данных от FastAPI)
    for model in models_list:
        prefix = "🟢 " if model == mdl_name else "⚪️ "
        markup.add(InlineKeyboardButton(f"{prefix}{model}", callback_data=model))

    # await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text = msg,
        reply_markup=markup,
        parse_mode="HTML"
    )
    await call.answer(f"🟢 Модель {mdl_name} выбрана!")


# +++++++++++++++ PHOTO +++++++++++++++
# handler for receiving images and making POST requests to FastAPI
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def process_image(message: types.Message):
    API_URL = os.getenv("API_URL")  #  получаем значение переменной API_URL из .env файла
    mdl_name = os.getenv("mdl_name")  #  получаем значение переменной mdl_name из .env файла

    file_id = message.photo[-1].file_id  # Получение файла изображения 
    file = await bot.get_file(file_id)  # Получение объекта файла 
    file_path = file.file_path  # Получение пути к файлу 
    # print(f'1 ......... {file_path}')

    image_data = await bot.download_file(file_path)  # Загрузка изображения

    url = f'{API_URL}/predict'  # Отправка изображения на сервер 
    # print(f'2 ====== {url}')

    timeout = ClientTimeout(total=15)  # Устанавливаем общий таймаут в 15 секунд
    async with aiohttp.ClientSession(timeout=timeout) as session:  # Инициализация асинхронной сессии HTTP
    # async with ClientSession() as session:  # Инициализация асинхронной сессии HTTP 
        form = aiohttp.FormData()  # Инициализация формы 
        form.add_field('file', image_data, filename='input_image.jpg', content_type='image/jpg')  # Добавление поля в форму 
        form.add_field('mdl_name', mdl_name)
        try:
            # async with session.post(url, data=form, timeout=30) as response:
            async with session.post(url, data=form) as response:
                # print(f'3 ====== {response.status}')
                if response.status == 200:
                    output_image_data = BytesIO(await response.read())
                    output_image_data.seek(0)
                    msg = f"✅ Обработанное изображение\nМодель: <b>{mdl_name}</b>"
                    await message.reply_photo(photo=output_image_data, caption=msg, parse_mode="HTML")
        except Exception as e:
            print(f"predict ------ ⛔️ Сервер недоступен: {e}")
            await message.answer(f"⛔️ Сервер <b>FastAPI [{API_URL}]</b> недоступен!\n⌛️ Timeout=<b>{timeout} s</b>\n{e}", parse_mode="HTML")

    #if response.status_code == 200:
    #    # Получение обработанного изображения и отправка его обратно пользователю
    #    output_image_data = BytesIO(response.content)
    #    output_image_data.seek(0)
    #    await message.reply_photo(photo=output_image_data, caption="Обработанное изображение")


# +++++++++++++++ TOOLS [/id, /list, /add, /help] +++++++++++++++
@dp.message_handler(commands=['id'])
async def send_welcome(message: types.Message):
    my_str = (f"👤 {message.from_user.full_name} [<code>{message.from_user.username}</code>] ->\n"
              f"🆔 <b>User ID:</b> <code>{message.from_user.id}</code>\n"
              f"👥 <b>Chat ID:</b> <code>{message.chat.id}</code>")
    await message.reply(my_str, parse_mode="HTML")


@dp.message_handler(lambda message: message.forward_from)
async def handle_forwarded_message(message: types.Message):
    original_user_id = message.forward_from.id
    chat_id = message.chat.id
    u_name = message.forward_from.username
    f_name = message.forward_from.full_name

    response_str = (f"👤 <b>{f_name}</b> [<code>@{u_name}</code>]  ->\n"
                    f"🆔 <b>Forwarded User ID:</b> <code>{original_user_id}</code>\n"
                    f"👥 <b>Chat ID:</b> <code>{chat_id}</code>")
    await message.reply(response_str, parse_mode="HTML")

@dp.message_handler(commands=['list'])
async def send_access_list(message: types.Message):
    ACCESS_LIST = os.getenv("ACCESS_LIST")
    if ACCESS_LIST:
        access_list = ACCESS_LIST.split(',')
        formatted_list = ' '.join([f"<code>{x.strip()}</code>" for x in access_list])
        await message.answer(f"❇️ <b>ACCESS_LIST</b>:\n{formatted_list}", parse_mode="HTML")
    else:
        await message.answer("⚠️ ACCESS_LIST пуст.", parse_mode="HTML")


@dp.message_handler(lambda message: message.text.startswith('/add'))
async def add_to_access_list(message: types.Message):
    user_command = message.text.split()
    if len(user_command) != 2:
        await message.answer("⚠️ Неверный формат. Используйте /add [ID].")
        return

    try:
        new_id = int(user_command[1])  # Попытка преобразовать введенный ID в число
    except ValueError:
        await message.answer("⚠️ ID должен быть числом. Попробуйте снова.")
        return

    ACCESS_LIST = os.getenv("ACCESS_LIST")  # Получаем текущий ACCESS_LIST из .env файла

    if ACCESS_LIST:
        access_list = list(map(int, ACCESS_LIST.split(',')))  # Преобразуем строку в список
    else:
        access_list = []

    if new_id not in access_list:  # Проверяем, является ли ID уникальным
        access_list.append(new_id)
        new_access_list = ','.join(map(str, access_list))
        update_env_variable('ACCESS_LIST', new_access_list)  # Сохраняем новый ACCESS_LIST в .env файл
        await message.answer("✅ Ваш ID был добавлен в ACCESS_LIST.")
    else:
        await message.answer("⚠️ Ваш ID уже есть в ACCESS_LIST.")


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_from_access_list(message: types.Message):
    user_command = message.text.split()[1:]  # Получаем все аргументы после '/del'

    if len(user_command) < 1:
        await message.answer("⚠️ Неверный формат. Используйте /del [ID1] [ID2] ...")
        return

    ACCESS_LIST = os.getenv("ACCESS_LIST")  # Получаем текущий ACCESS_LIST из .env файла

    if ACCESS_LIST:
        access_list = list(map(int, ACCESS_LIST.split(',')))  # Преобразуем строку в список
    else:
        await message.answer("⚠️ ACCESS_LIST пуст.")
        return

    deleted_ids = []
    not_found_ids = []

    for str_id in user_command:
        try:
            del_id = int(str_id)  # Попытка преобразовать ID для удаления в число
        except ValueError:
            await message.answer(f"⚠️ ID {str_id} должен быть числом. Пропускаем.")
            continue

        if del_id in access_list:  # Проверяем, существует ли ID в ACCESS_LIST
            access_list.remove(del_id)
            deleted_ids.append(str(del_id))
        else:
            not_found_ids.append(str(del_id))

    if deleted_ids:
        new_access_list = ','.join(map(str, access_list))
        update_env_variable('ACCESS_LIST', new_access_list)  # Сохраняем новый ACCESS_LIST в .env файл
        await message.answer(f"❎ ID {', '.join(deleted_ids)} успешно удалены из ACCESS_LIST.")

    if not_found_ids:
        await message.answer(f"⚠️ ID {', '.join(not_found_ids)} не найдены в ACCESS_LIST.")


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer(help_text, parse_mode="Markdown")


# +++++++++++++ MAIN +++++++++++++
async def main():
    await on_startup(dp)
    await dp.start_polling()  # Запуск бота 

if __name__ == '__main__':
    asyncio.run(main())
