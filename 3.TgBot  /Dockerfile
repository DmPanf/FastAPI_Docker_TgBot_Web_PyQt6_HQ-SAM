# Dockerfile Use a lightweight Python image

FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# библиотека libGL.so.1 необходима для работы модуля OpenCV (cv2)
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Upgrade pip with no cache # Один RUN лучше, чем множество RUN команд для уменьшения количества слоев в Docker-образе
RUN pip install --no-cache-dir -U pip aiogram

# Copy data & code into the container
COPY . /app

# Установка дополнительных зависимостей, указанных в requirements.txt (если они есть)
RUN if [ -f "requirements.txt" ]; then pip install --no-cache-dir -r requirements.txt; fi

# Run your bot script
CMD ["python", "bot_code.py"]
