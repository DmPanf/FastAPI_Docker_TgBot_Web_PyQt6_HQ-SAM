# python tools.py
# 

import json
from aiogram import Bot
from dotenv import load_dotenv
import os


load_dotenv()
CHAT_ID = os.getenv("CHAT_ID")

def load_servers_list(bot: Bot):
    try:
        with open("config.json", "r") as config_file:
            config_data = json.load(config_file)
            servers_list = config_data.get("servers", [])

        if servers_list is None:
            bot.send_message(chat_id=CHAT_ID, text="⛔ Ошибка: ключ 'servers' отсутствует в config.json.")
            return None

        # Проверим, является ли servers_list списком
        if not isinstance(servers_list, list):
            bot.send_message(chat_id=CHAT_ID, text="⛔ Ошибка: 'servers' должен быть списком.")
            return None

        return servers_list

    except json.JSONDecodeError:
        bot.send_message(chat_id=CHAT_ID, text="⛔ Ошибка: config.json не содержит корректный JSON-объект.")
        return None


    
def update_env_variable(key, new_value):
    # Читаем текущий .env файл и сохраняем его содержимое в словарь
    env_variables = {}
    with open('.env', 'r') as f:
        for line in f.readlines():
            k, v = line.strip().split('=', 1)
            env_variables[k] = v

    # Обновляем значение переменной
    env_variables[key] = new_value

    # Записываем обновленные переменные обратно в .env файл
    with open('.env', 'w') as f:
        for k, v in env_variables.items():
            f.write(f"{k}={v}\n")

    # Обновляем значение в текущем процессе в переменной окружения!!!
    os.environ[key] = new_value
