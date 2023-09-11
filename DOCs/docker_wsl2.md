## 
### Шаг 1: Установка Docker Desktop
1. Перейдите на [официальный сайт Docker](https://www.docker.com/products/docker-desktop) и скачайте Docker Desktop для Windows.
2. Установите Docker Desktop, следуя инструкциям.

### Шаг 2: Включение WSL 2
1. Откройте PowerShell от имени администратора.
2. Введите команду `wsl --set-default-version 2` для установки WSL 2 по умолчанию.

### Шаг 3: Установка Nvidia-Docker (если у вас есть GPU от Nvidia)
- Перейдите на [GitHub репозиторий Nvidia-Docker](https://github.com/NVIDIA/nvidia-docker) и следуйте инструкциям.

### Шаг 4: Создание Dockerfile
- Такой же `Dockerfile`, как и в инструкции для Ubuntu, должен сработать и здесь.

### Шаг 5: Создание docker-compose.yml
- Аналогично, используйте такой же `docker-compose.yml` файл.

### Шаг 6: Сборка и запуск контейнера
1. Откройте PowerShell или терминал в директории, где находятся ваш `Dockerfile` и `docker-compose.yml`.
2. Введите `docker-compose build` для сборки образа.
3. Введите `docker-compose up` для запуска контейнера.

### Дополнительно
- Если вы хотите использовать GPU, убедитесь, что ваш `docker-compose.yml` включает в себя `runtime: nvidia` и соответствующие переменные окружения.
