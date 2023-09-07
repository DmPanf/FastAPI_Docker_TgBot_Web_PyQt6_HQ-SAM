import json

def format_file_size(size_in_bytes):
    # size_in_bytes должно быть числом (размером файла в байтах)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} TB"

def server_address():
    # Загружаем список серверов из файла конфигурации
    with open("config.json", "r") as config_file:
        config_data = json.load(config_file)  # Открываем файл конфигурации 
        servers = config_data.get("servers", [])  # Получаем список серверов 
    
    return servers
