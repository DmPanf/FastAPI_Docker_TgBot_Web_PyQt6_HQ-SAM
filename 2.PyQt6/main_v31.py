# python main_v31.py
# Загрузка и Predict по постоянным константам: ссылке и модели

import sys  # модуль для работы с операционной системой
import os  # модуль для работы с операционной системой 
import requests  # модуль для отправки запросов на сервер
import json  # модуль для работы с JSON форматом
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QSizePolicy)
from PyQt6.QtWidgets import (QFileDialog, QRadioButton, QDialog)  # модуль для работы с виджетами 
from PyQt6.QtCore import Qt, QSize # модуль для работы с размерами элементов виджета 
from PyQt6.QtGui import QPixmap, QFont, QPalette, QColor  # модуль для работы с изображениями 
from menu_styles import borderStyle, btnStyle  # модуль для оформления виджетов и кнопок
from ModelDialog import ModelDialog  # модуль для диалогового окна Выбора Модели из списка
from ServerDialog import ServerDialog  # модуль для диалогового окна Выбора Сервера из списка
from tools import format_file_size  # модуль для форматирования размера файла


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        #dialog = ServerDialog()  # Создаем диалоговое окно для выбора сервера
        #result = dialog.exec()
        #self.Server = dialog.selected_server
        self.Server = "http://api-serv.ru:8001"

        #if result == QDialog.DialogCode.Accepted:
        #    print("Выбранный сервер:", self.Server)
        #    # Здесь можно выполнить запрос к FastAPI и обновить self.infoLabel
        #else:
        #    print("Отменено")

        global mdl_name  # Устанавливаем имя модели в глобальную переменную mdl_name

    def initUI(self):
        # Настройка основного окна
        self.setWindowTitle("X-Rays Model HQ-SAM App [v2.1, 2023]")
        self.setGeometry(100, 100, 600, 800)
        self.center()

        # Создание виджетов
        centralWidget = QWidget(self)  # Создание виджета QWidget 
        mainLayout = QVBoxLayout()  # Создание виджета QVBoxLayout 

        # Виджет для изображения
        self.imageLabel = QLabel(self) # Создание виджета QLabel - изображение 
        self.imageLabel.setFixedSize(596, 660)  # Установка размеров для виджета изображений
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
        btnLoad = QPushButton("IMAGE LOAD", self)  # 
        btnLoad.clicked.connect(self.loadImage)  # Выбор и загрузка изображения с локального диска
        btnLoad.setStyleSheet(btnStyle)  # Оформление кнопки 

        btnPredict = QPushButton("PREDICT", self)  # 
        btnPredict.clicked.connect(self.predict_image)  # Отправка изображения на обработку по запросу через FastAPI
        btnPredict.setStyleSheet(btnStyle)  # Оформление кнопки 

        btnModels = QPushButton("MODELS", self)
        btnModels.clicked.connect(self.loadModels)  # Загрузка моделей по запросу через FastAPI
        btnModels.setStyleSheet(btnStyle)  # Оформление кнопки

        btnSave = QPushButton("SAVE", self)
        btnSave.clicked.connect(self.saveImage)  # Сохранение обработанного изображения на диске
        btnSave.setStyleSheet(btnStyle)  # Оформление кнопки 

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(btnLoad)
        buttonLayout.addWidget(btnPredict)
        buttonLayout.addWidget(btnModels)
        buttonLayout.addWidget(btnSave)

        # создание и добавление виджетов
        mainLayout.addLayout(buttonLayout)
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

    def center(self):
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    def loadImage(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg);;All Files (*)")
        if filePath:
            pixmap = QPixmap(filePath)
            # Установка изображения для imageLabel
            #self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.width(), self.imageLabel.height(), Qt.AspectRatioMode.KeepAspectRatio))
            #scaled_pixmap = pixmap.scaled(self.imageLabel.size(), Qt.AspectRatioMode.KeepAspectRatio)
            # self.imageLabel.setPixmap(scaled_pixmap)
            self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

            # Получение размеров изображения
            width = pixmap.width()
            height = pixmap.height()
            # Получение размера файла
            file_size = os.path.getsize(filePath)
            readable_size = format_file_size(file_size)
            self.infoLabel.setText(f"⚙️ Файл: {filePath.split('/')[-1]},\n⚙️ Размер файла: {readable_size},\n⚙️ Размеры изображения: {width}x{height}")


    def predict_image(self):
        # Путь к загруженному изображению (test)
        image_path = "./images/001.jpg"
        
        # Выбор Сервера и запрос списк моделей через API
        self.Server = ServerDialog()
        API_URL_PREDICT = self.Server + "/predict"
        mdl_name = self.loadModels()
        
        # Отправка изображения на сервер для предсказания
        with open(image_path, "rb") as image_file:
            files = {"file": ("image.jpg", image_file)}
            data = {"mdl_name": mdl_name}
            response = requests.post(API_URL_PREDICT, files=files, data=data)
            
            if response.status_code == 200:
                # Отображение предсказанного изображения
                image_data = response.content
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                self.imageLabel.setPixmap(pixmap)
                self.infoLabel.setText("Изображение предсказано!")
            else:
                self.infoLabel.setText("Ошибка при предсказании изображения")

    def loadModels(self):
        # Запрос к FastAPI для получения списка доступных моделей
        API_URL_MODELS = self.Server + "/models"
        try:
            response = requests.get(API_URL_MODELS)
            if response.status_code == 200:
                data = response.json()
                available_models = data.get("Models", [])
                if available_models:
                    # Создаем и отображаем диалоговое окно с выбором модели
                    dialog = ModelDialog(available_models, self)
                    result = dialog.exec()
                    mdl_name = dialog.selected_model

                    if result == QDialog.DialogCode.Accepted:
                        # Выбранная модель сохранена в переменной mdl_name
                        print("Выбранная модель:", mdl_name)
                    else:
                        print("Отменено")
                else:
                    print("Нет доступных моделей.")
            else:
                print("Ошибка при получении списка моделей:", response.status_code)
        except Exception as e:
            print("Ошибка при запросе к FastAPI:", str(e))


    def saveImage(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
