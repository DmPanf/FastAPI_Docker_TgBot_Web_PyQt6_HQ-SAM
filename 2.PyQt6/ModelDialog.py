# ModelDialog.py

from PyQt6.QtCore import QSize  # модуль для работы с размерами элементов виджета 
from PyQt6.QtGui import QPixmap, QFont  # модуль для работы с изображениями 
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QRadioButton, QPushButton
from menu_styles import radiobtnStyle, menubtnStyle # модуль для оформления виджетов и кнопок 


class ModelDialog(QDialog):
    def __init__(self, available_models, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выберите модель")
        self.setGeometry(100, 100, 300, 240)  # Устанавливаем размеры диалогового окна

        self.setLayout(QVBoxLayout())

        self.radio_buttons = []
        
        # Создаем радиокнопки для каждой доступной модели с крупным шрифтом
        font = QFont()
        font.setPointSize(16)  # Устанавливаем крупный размер шрифта

        # Создаем радиокнопки для каждой доступной модели
        for model_name in available_models:
            radio_button = QRadioButton(model_name, self)
            radio_button.setFont(font)  # Устанавливаем крупный шрифт для радиокнопки
            radio_button.setIconSize(QSize(50, 50))  # Устанавливаем размер иконки радиокнопки
            radio_button.setStyleSheet(radiobtnStyle)  # Увеличиваем размер радиокнопки и устанавливаем отступы
            self.radio_buttons.append(radio_button)
            self.layout().addWidget(radio_button)

        # Кнопки "Cancel" и "Set Model"
        button_layout = QHBoxLayout()
        font.setPointSize(12)  # Устанавливаем крупный размер шрифта для кнопок
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
        # mdl_name  # Устанавливаем выбранное имя модели в глобальную переменную mdl_name
        mdl_name = selected_radio_button.text()
        self.accept()     # Закрываем диалоговое окно
        return mdl_name

