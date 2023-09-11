Я могу предложить общий шаг-за-шагом план для установки и интеграции YOLO, OpenCV, и Pillow с использованием Docker и docker-compose на Ubuntu Linux. Используя GPU типа Nvidia GeForce RTX 3060-3090, этот подход должен быть довольно эффективным.

### Предварительные шаги:

1. **Установка Docker и Docker-Compose**
    - Установка Docker: `sudo apt update && sudo apt install docker.io`
    - Установка Docker Compose: `sudo apt install docker-compose`

2. **Установка Nvidia-Docker**
    - Следуйте инструкциям с [официального сайта](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html).

### Создание `Dockerfile`

Создайте файл с именем `Dockerfile`:

```Dockerfile
# Используем базовый образ с поддержкой CUDA для Nvidia
FROM nvidia/cuda:11.0-base

# Устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libopencv-dev

# Установим Python библиотеки
RUN pip3 install opencv-python pillow

# Клонируем YOLO
RUN git clone https://github.com/AlexeyAB/darknet.git
WORKDIR /darknet

# Собираем YOLO
RUN make

# Копируем предобученные веса
RUN wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights .

# Настройки для GPU
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

### Создание `docker-compose.yml`

```yml
version: '3'
services:
  yolo-service:
    build: .
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
```

### Сборка и запуск контейнера

1. Собираем образ: `docker-compose build`
2. Запускаем контейнер: `docker-compose up`
