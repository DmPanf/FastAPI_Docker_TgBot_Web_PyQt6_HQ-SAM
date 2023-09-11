## 

### Шаг 1: Установка Docker и Docker-Compose
1. Откройте терминал и выполните следующие команды:
    - Обновление пакетов: `sudo pacman -Syu`
    - Установка Docker: `sudo pacman -S docker`
    - Запуск Docker: `sudo systemctl start docker`
    - Установка Docker Compose: `sudo pacman -S docker-compose`

### Шаг 2: Установка Nvidia-Docker (если у вас есть Nvidia GPU)
- Следуйте инструкциям на [официальном сайте](https://github.com/NVIDIA/nvidia-docker) для установки nvidia-docker.

### Шаг 3: Создание Dockerfile
- Создайте файл `Dockerfile` с тем же содержанием, что и в инструкции для Ubuntu.

### Шаг 4: Создание docker-compose.yml
- Создайте файл `docker-compose.yml` аналогично инструкции для Ubuntu.

```yaml
version: '3'
services:
  yolo-service:
    build: .
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
```

### Шаг 5: Сборка и запуск контейнера
1. Откройте терминал в директории, где находятся ваш `Dockerfile` и `docker-compose.yml`.
2. Соберите Docker образ: `docker-compose build`
3. Запустите контейнер: `docker-compose up`
