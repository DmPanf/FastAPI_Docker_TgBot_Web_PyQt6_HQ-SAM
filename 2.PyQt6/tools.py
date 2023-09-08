import json  # модуль для работы с JSON форматом
import os  # модуль для работы с операционной системой 
from PIL import Image  # модуль для работы с изображениями 
import io  # модуль для работы с потоками 

def format_file_size(size_in_bytes):  # функция форматирования размера файла 
    # size_in_bytes должно быть числом (размером файла в байтах)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} TB"

def server_address():  # функция получения списка серверов из файла конфигурации 
    # Загружаем список серверов из файла конфигурации
    with open("config.json", "r") as config_file:
        config_data = json.load(config_file)  # Открываем файл конфигурации 
        servers = config_data.get("servers", [])  # Получаем список серверов 
    
    return servers

def save_predicted_image(image_data):  # функция сохранения предсказанного изображения в файле 
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Получаем список всех файлов в папке output
    files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]

    # Отфильтровываем файлы, которые начинаются с "predicted_"
    predicted_files = [f for f in files if f.startswith('predicted_')]

    max_index = -1
    for file in predicted_files:
        try:
            index = int(file.split('_')[1].split('.')[0])
            max_index = max(max_index, index)
        except ValueError:
            pass

    next_index = max_index + 1
    next_filename = os.path.join(output_dir, f'predicted_{next_index:03d}.jpg')

    # Сохраняем изображение
    image = Image.open(io.BytesIO(image_data))
    image.save(next_filename)

    print(f"💾 Saved image to {next_filename}")
    return next_filename
