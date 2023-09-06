# ServerDialog.py
from PyQt6.QtCore import QSize  # модуль для работы с размерами элементов виджета 
from PyQt6.QtGui import QPixmap, QFont  # модуль для работы с изображениями 
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QRadioButton, QPushButton
from menu_styles import radiobtnStyle, menubtnStyle # модуль для оформления виджетов и кнопок 
from tools import server_address


class ServerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.servers = server_address()  # Получаем список серверов 
        self.setWindowTitle("Выберите сервер")
        self.setGeometry(100, 100, 300, 240)  # Устанавливаем размеры диалогового окна

        self.setLayout(QVBoxLayout())

        self.radio_buttons = []

        # Создаем радиокнопки для каждого сервера с крупным шрифтом и стилем
        font = QFont()
        font.setPointSize(14)  # Устанавливаем крупный размер шрифта

        for server in self.servers:
            server_name = server["name"]
            radio_button = QRadioButton(server_name, self)
            radio_button.setFont(font)  # Устанавливаем крупный размер шрифта для радиокнопки
            radio_button.setStyleSheet("QRadioButton { color: green; background-color: lightgray; }")  # Зеленый цвет текста и светлосерый фон
            radio_button.setIconSize(QSize(20, 20))  # Устанавливаем размер иконки радиокнопки
            self.radio_buttons.append(radio_button)
            self.layout().addWidget(radio_button)

        # Кнопки "Cancel" и "Select Server" с крупным шрифтом
        button_layout = QHBoxLayout()
        font.setPointSize(16)  # Устанавливаем крупный размер шрифта для кнопок
        cancel_button = QPushButton("Cancel", self)
        select_server_button = QPushButton("Select Server", self)
        cancel_button.setFont(font)
        select_server_button.setFont(font)
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(select_server_button)

        self.layout().addLayout(button_layout)

        # Обработчик нажатия кнопки "Select Server"
        select_server_button.clicked.connect(self.select_server)

        # Обработчик нажатия кнопки "Cancel"
        cancel_button.clicked.connect(self.reject)

    def select_server(self):
        # Находим выбранную радиокнопку 
        selected_radio_button = next(radio_button for radio_button in self.radio_buttons if radio_button.isChecked())

        # Получаем информацию о выбранном сервере
        selected_server_name = selected_radio_button.text()  # Получаем имя выбранного сервера 
        selected_server = next((server for server in self.servers if server["name"] == selected_server_name), None)  # Получаем информацию о выбранном сервере

        self.accept()  # Закрываем диалоговое окно
        return selected_server if selected_server else "http://api-serv.ru:8001"
