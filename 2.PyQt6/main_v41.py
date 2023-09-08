# Загрузка и Predict по постоянным константам: ссылке и модели
import sys  # модуль для работы с операционной системой
import os  # модуль для работы с операционной системой 
import requests  # модуль для отправки запросов на сервер
from requests.exceptions import ConnectionError, Timeout, RequestException  # модуль для обработки ошибок
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QSizePolicy)
from PyQt6.QtWidgets import (QFileDialog, QDialog, QMessageBox)  # модуль для работы с виджетами 
from PyQt6.QtCore import Qt  # модуль для работы с размерами элементов виджета 
from PyQt6.QtGui import QPixmap  # модуль для работы с изображениями 
from menu_styles import borderStyle, btnStyle  # модуль для оформления виджетов и кнопок
from ModelDialog import ModelDialog  # модуль для диалогового окна Выбора Модели из списка
from ServerDialog import ServerDialog  # модуль для диалогового окна Выбора Сервера из списка
from tools import format_file_size, save_predicted_image  # модуль для форматирования размера файла


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.mdl_name = None  # Имя модели для диалогового окна
        self.image_data = None  # Изображение для диалогового окна
        self.select_server()

    def select_server(self):
        while True:
            dialog = ServerDialog()  # Создаем диалоговое окно для выбора сервера
            result = dialog.exec()

            if hasattr(dialog, 'selected_server_url'):  # Проверяем, установлен ли атрибут selected_server_url
                self.Server = dialog.selected_server_url
            else:
                self.Server = "http://localhost:8001"  # Значение по умолчанию

            if result == QDialog.DialogCode.Accepted:
                try:
                    print(f"❇️ Выбранный сервер: {self.Server}")
                    # Здесь выполняем запрос к FastAPI и обновляем self.infoLabel
                    project_name = self.request_project_name()  # Получаем имя проекта с сервера 
                    self.infoLabel.setText(f"{project_name}\n♻️ Выбран сервер: {self.Server}")
                    break  # выход из цикла, если все прошло успешно
                except ConnectionError:
                    print("❌ Connection error. Please check if the FastAPI server is running.")
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Icon.Warning)
                    msg.setText("⚠️ Ошибка соединения.")
                    msg.setWindowTitle("Ошибка")
                    msg.exec()
            else:
                print("⛔️ Отменено")
                break  # выход из цикла, если пользователь нажал "Cancel"

    def update_model_name(self, mdl_name):    # +++++ Создаем новый слот для обновления self.mdl_name !!! +++++
        # print(f" ===== Updating model name: {mdl_name}")
        self.mdl_name = mdl_name
        oldText = self.infoLabel.text()
        self.infoLabel.setText(f"{oldText}\n♻️ Выбрана модель: {mdl_name}")

    def initUI(self):
        # Настройка основного окна
        self.setWindowTitle("X-Rays Model HQ-SAM App [v2.1, 2023]")  # Название окна 
        self.setGeometry(100, 100, 640, 800)  # Размеры окна 
        self.center()  # Расположение окна в центре экрана 

        # Создание виджетов
        centralWidget = QWidget(self)  # Создание виджета QWidget 
        mainLayout = QVBoxLayout()  # Создание виджета QVBoxLayout 

        # Виджет для изображения
        self.imageLabel = QLabel(self) # Создание виджета QLabel - изображение 
        self.imageLabel.setFixedSize(638, 660)  # Установка размеров для виджета изображений
        self.imageLabel.setStyleSheet(borderStyle) # Установка стиля для виджета изображения 
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Выравнивание изображения по центру виджета
        self.imageLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Позволяет QLabel растягиваться

        # Виджет для вывода информации
        self.infoLabel = QLabel("Выберите изображение", self)  # Создание виджета QLabel 
        self.infoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Выравнивание изображения по центру виджета

        # Центрирование виджета изображения
        imageLayout = QHBoxLayout()  # Создание виджета QHBoxLayout - расположение виджета изображения на экране 
        imageLayout.addStretch(1)  # Эти растягивания обеспечивают центрирование виджета с изображением
        mainLayout.addLayout(imageLayout, 8)  # 8 частей из 9 для виджета изображения
        mainLayout.addWidget(self.infoLabel, 1)  # 1 часть из 9 для виджета с информацией

        # создание и добавление кнопок 
        btnLoad = QPushButton("IMAGE LOAD", self)  # self указывает, что эта кнопка будет дочерним элементом текущего окна или виджета, в котором она создается
        btnLoad.clicked.connect(self.loadImage)  # Выбор и загрузка изображения с локального диска
        btnLoad.setStyleSheet(btnStyle)  # Оформление кнопки 

        btnPredict = QPushButton("PREDICT", self)  # self указывает, что эта кнопка будет дочерним элементом текущего окна или виджета, в котором она создается
        btnPredict.clicked.connect(self.predict_image)  # Отправка изображения на обработку по запросу через FastAPI
        btnPredict.setStyleSheet(btnStyle)  # Оформление кнопки 

        btnModels = QPushButton("MODELS", self) # self указывает, что эта кнопка будет дочерним элементом текущего окна или виджета, в котором она создается
        btnModels.clicked.connect(self.loadModels)  # Загрузка моделей по запросу через FastAPI
        btnModels.setStyleSheet(btnStyle)       # Оформление кнопки

        btnSave = QPushButton("SAVE", self)     # создает новую кнопку в PyQt6 с надписью "SAVE"
        btnSave.clicked.connect(self.saveImage) # Сохранение обработанного изображения на диске
        btnSave.setStyleSheet(btnStyle)         # Оформление кнопки 

        buttonLayout = QHBoxLayout()            # Создание виджета QHBoxLayout - расположение кнопок на экране 
        buttonLayout.addWidget(btnLoad)         # Добавление кнопки IMAGE LOAD
        buttonLayout.addWidget(btnModels)       # Добавление кнопки MODELS
        buttonLayout.addWidget(btnPredict)      # Добавление кнопки PREDICT
        buttonLayout.addWidget(btnSave)         # Добавление кнопки SAVE

        # создание и добавление виджетов
        mainLayout.addLayout(buttonLayout)      # Добавление кнопок на экран 
        centralWidget.setLayout(mainLayout)     # Установка виджета на основной виджет
        self.setCentralWidget(centralWidget)    # Установка основного виджета

    def center(self):
        #screen = QApplication.primaryScreen().geometry()
        #size = self.geometry()
        #self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

        screen_geometry = QApplication.primaryScreen().geometry()  # Получаем геометрию главного экрана
        window_geometry = self.frameGeometry()  # Получаем геометрию окна
        center_point = screen_geometry.center()  # Находим центр экрана
        window_geometry.moveCenter(center_point)  # Устанавливаем центр окна в центр экрана
        window_geometry.moveTop(window_geometry.top() - 10)  # Добавляем смещение: отодвигаем окно вверх на 10 пикселей
        self.move(window_geometry.topLeft())  # Перемещаем окно

    def loadImage(self):  # Загрузка изображения из локального диска 
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg);;All Files (*)")
        if filePath:  # Если пользователь выбрал файл 
            self.filePath = filePath  # Сохраняем путь к файлу как атрибут класса
            pixmap = QPixmap(self.filePath)  # Создание QPixmap из выбранного изображения 
            # Установка изображения для imageLabel
            #self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.width(), self.imageLabel.height(), Qt.AspectRatioMode.KeepAspectRatio))
            #scaled_pixmap = pixmap.scaled(self.imageLabel.size(), Qt.AspectRatioMode.KeepAspectRatio)
            # self.imageLabel.setPixmap(scaled_pixmap)
            self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

            # Получение размеров изображения
            width = pixmap.width()
            height = pixmap.height()
            # Получение размера файла
            file_size = os.path.getsize(self.filePath)  
            readable_size = format_file_size(file_size)  # Форматирование размера файла 
            self.infoLabel.setText(f"⚙️ Файл: {self.filePath.split('/')[-1]},\n⚙️ Размер файла: {readable_size},\n⚙️ Размеры изображения: {width}x{height}")


    def predict_image(self):
        try:
            if self.mdl_name is None:
                print(" ----- Model is not selected.")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setText("⚠️ Модель не выбрана.")
                msg.setWindowTitle("Ошибка")
                msg.exec()
                return

            if not hasattr(self, 'filePath'):
                print(" ===== Image is not loaded.")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setText("⚠️ Изображение не загружено.")
                msg.setWindowTitle("Ошибка")
                msg.exec()
                return
        
            API_URL_PREDICT = f"{self.Server}/predict"
            #self.mdl_name = self.loadModels()
            
            # Отправка изображения на сервер для предсказания
            with open(self.filePath, "rb") as image_file:  # Открытие изображения в бинарном режиме 
                files = {"file": ("image.jpg", image_file)}  # Отправка изображения на сервер 
                data = {"mdl_name": self.mdl_name}  # Отправка модели на сервер 
                response = requests.post(API_URL_PREDICT, files=files, data=data, timeout=10)  # Отправка запроса 
                
                if response.status_code == 200:  # Если запрос выполнен успешно 
                    # Отображение предсказанного изображения
                    self.image_data = response.content  # Получение ответа с сервера 
                    pixmap = QPixmap()  # Создание QPixmap из полученного изображения 
                    pixmap.loadFromData(self.image_data)  # Загрузка полученного изображения в QPixmap 
                    self.imageLabel.setPixmap(pixmap)  # Установка изображения для imageLabel 
                    self.infoLabel.setText("Изображение предсказано!")  # Отображение предсказанного изображения 
                else:
                    self.infoLabel.setText("Ошибка при предсказании изображения")  # Ошибка при предсказании изображения

        except ConnectionError:
            print("❌ Connection error. Please check if the FastAPI server is running.")
        except Timeout:
            print("⭕️ Request timed out.")
        except RequestException as error:
            print(f"🆘 An error occurred while making the request: {error}")


    def request_project_name(self):
        API_URL_INFO = f"{self.Server}/info"
        try:
            response = requests.get(API_URL_INFO)  # Отправка запроса 
            if response.status_code == 200:  # Если запрос выполнен успешно
                data = response.json()  # Получение ответа с сервера
                project_name = data.get("Project 2023")  # Получение имени проекта
                #print("🔘 Response: ", project_name)
                return project_name  # Возврат имени проекта
            else:
                return f"🔘 Response: {response}"
        except Exception as e:
            print("⛔️ Ошибка при получении имени проекта:", e)

    def loadModels(self):
        # Запрос к FastAPI для получения списка доступных моделей
        API_URL_MODELS = f"{self.Server}/models"

        try:
            response = requests.get(API_URL_MODELS)  # Отправка запроса 
            if response.status_code == 200:  # Если запрос выполнен успешно 
                data = response.json()  # Получение ответа с сервера 
                available_models = data.get("Models", [])  # Получение списка доступных моделей 
                if available_models:  # Если список доступных моделей не пуст 
                    # Создаем и отображаем диалоговое окно с выбором модели
                    dialog = ModelDialog(available_models, self)

                    # +++++ При создании dialog, подключаем сигнал к слоту !!!!! +++++
                    dialog.model_selected.connect(self.update_model_name)

                    result = dialog.exec()  # Отображение диалогового окна 
                    if result == QDialog.DialogCode.Accepted:  # Если пользователь выбрал модель из списка 
                        print("✅ Выбранная модель:", self.mdl_name)  # Отображение выбранной модели 
                    else:
                        print("❌ Отменено")  # Отображение отмены выбора модели 
                else:
                    print("⭕️ Нет доступных моделей.")  # Отображение, что нет доступных моделей 
            else:
                print("⛔️ Ошибка при получении списка моделей:", response.status_code)  # Ошибка при получении списка моделей 
        except Exception as e:
            print("🆘 Ошибка при запросе к FastAPI:", str(e))  # Ошибка при запросе к FastAPI


    def saveImage(self):
        if self.image_data is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("⚠️ Изображение для сохранения не найдено.")
            msg.setWindowTitle("Ошибка")
            msg.exec()
            return

        filename = save_predicted_image(self.image_data)  # Предполагается, что эта функция сохраняет изображение и возвращает имя файла
        if filename:  # Если файл успешно сохранен
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText(f"📥 Файл успешно сохранен в локальную папку.")
            msg.setInformativeText(f"Путь: ./{filename}")
            msg.setWindowTitle("💾 Сохранение завершено")
            msg.exec()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("⛔️ Ошибка при сохранении файла.")
            msg.setInformativeText("Пожалуйста, попробуйте еще раз.")
            msg.setWindowTitle("Ошибка")
            msg.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
