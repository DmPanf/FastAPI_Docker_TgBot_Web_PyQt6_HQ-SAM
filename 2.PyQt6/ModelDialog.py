# ModelDialog.py
from PyQt6.QtCore import pyqtSignal, QSize  # модули для работы с сигналами и с размерами элементов виджета
from PyQt6.QtGui import QFont  # модуль для работы с изображениями 
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QRadioButton, QPushButton
from menu_styles import radiobtnStyle, menubtnStyle # модуль для оформления виджетов и кнопок 

class ModelDialog(QDialog):
    model_selected = pyqtSignal(str)  # Создаем новый сигнал, который будет передавать строку

    def __init__(self, available_models, parent=None): # Определение конструктора с параметрами available_models и parent
        super().__init__(parent)  # Вызываем конструктор родительского класса и передаем ему параметр parent
        self.initUI(available_models)  # Инициализируем диалоговое окно (пользовательский интерфейс) 

    def initUI(self, available_models):  # Функция инициализации диалогового окна 
        self.setWindowTitle("Выберите модель")
        self.setGeometry(100, 100, 300, 240)  # Устанавливаем размеры диалогового окна

        self.setLayout(QVBoxLayout())
    
        # 🔘 Создаем радиокнопки для каждой доступной модели с крупным шрифтом
        self.radio_buttons = []
        font = QFont()
        font.setPointSize(16)  # Устанавливаем крупный размер шрифта

        for model_name in available_models:  # Создаем радиокнопки для каждой доступной модели
            radio_button = QRadioButton(model_name, self)
            radio_button.setFont(font)  # Устанавливаем крупный шрифт для радиокнопки
            radio_button.setIconSize(QSize(50, 50))  # Устанавливаем размер иконки радиокнопки
            #radio_button.setStyleSheet(radiobtnStyle)  # Увеличиваем размер радиокнопки и устанавливаем отступы
            #radio_button.setStyleSheet("QRadioButton { color: green; background-color: lightgray; }")  # Зеленый цвет текста и светлосерый фон
            radio_button.setStyleSheet("QRadioButton { color: lightgray; padding: 5px; font-weight: bold; }")
            radio_button.setChecked(True)  # По умолчанию выбран последний сервер
            self.radio_buttons.append(radio_button)
            self.layout().addWidget(radio_button)

        # 🔘 Кнопки "Cancel" и "Set Model"
        button_layout = QHBoxLayout()
        cancel_button = QPushButton("Cancel", self)
        cancel_button.setFont(font)
        cancel_button.setStyleSheet(menubtnStyle)  # Установка стиля кнопки 

        set_model_button = QPushButton("Set Model", self)
        set_model_button.setFont(font)
        set_model_button.setStyleSheet(menubtnStyle)  # Установка стиля кнопки

        button_layout.addWidget(cancel_button)
        button_layout.addWidget(set_model_button)

        self.layout().addLayout(button_layout)
        set_model_button.clicked.connect(self.set_model)  # Обработчик нажатия кнопки "Set Model"
        cancel_button.clicked.connect(self.reject)  # Обработчик нажатия кнопки "Cancel"

    def set_model(self):
        # Находим выбранную радиокнопку
        selected_radio_button = next(radio_button for radio_button in self.radio_buttons if radio_button.isChecked())
        self.mdl_name = selected_radio_button.text()
        print(f'\b+++ Выбранная модель: {self.mdl_name}')
        self.model_selected.emit(self.mdl_name)  # Испускаем сигнал с выбранной моделью
        self.accept()     # Закрываем диалоговое окно

