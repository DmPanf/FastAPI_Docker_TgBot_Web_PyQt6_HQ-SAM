# ServerDialog.py
from PyQt6.QtCore import Qt, QSize  # модуль для работы с размерами элементов виджета 
from PyQt6.QtGui import QFont, QMovie  # модуль для работы с изображениями 
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QRadioButton, QPushButton, QApplication, QLabel
from menu_styles import radiobtnStyle, btnStyle, borderStyle # модуль для оформления виджетов и кнопок 
from tools import server_address


class ServerDialog(QDialog):
    def __init__(self, parent=None):  # Определение конструктора с одним опциональным параметром parent
        super().__init__(parent)   # Вызываем конструктор родительского класса и передаем ему параметр parent
        self.servers = server_address()  # Получаем список серверов
        self.initUI()  # Инициализируем диалоговое окно (пользовательский интерфейс)
        self.center()  # Расположение окна в центре экрана

    def initUI(self):  # Функция инициализации диалогового окна 
        self.setWindowTitle("📡 Выберите сервер")
        self.setGeometry(100, 100, 500, 380)  # Устанавливаем размеры диалогового окна

        self.setLayout(QVBoxLayout())
        # Создание QLabel для отображения GIF
        self.movie_label = QLabel(self)
        # self.movie_label.setStyleSheet(borderStyle) # Установка стиля для виджета изображения
        self.movie = QMovie("./images/main.gif")
        self.movie_label.setMovie(self.movie)

        # Задаем размеры для QLabel с сохранением пропорций
        #self.movie_label.setFixedSize(QSize(500, 400))

        self.movie.start()   
        self.layout().addWidget(self.movie_label)  # Добавляем QLabel в виджет      

        # 🔘 Создаем радиокнопки для каждого сервера с крупным шрифтом и стилем
        self.radio_buttons = []
        font = QFont()
        font.setPointSize(16)  # Устанавливаем крупный размер шрифта

        for server in self.servers:  # Создаем радиокнопки для каждого сервера из файла конфигурации
            server_name = server["name"]
            radio_button = QRadioButton(server_name, self)
            radio_button.setFont(font)  # Устанавливаем крупный размер шрифта для радиокнопки
            #radio_button.setStyleSheet("QRadioButton { color: green; background-color: lightgray; }")  # Зеленый цвет текста и светлосерый фон
            radio_button.setStyleSheet("QRadioButton { color: lightgray; padding: 5px; font-weight: bold; }")
            #radio_button.setStyleSheet(radiobtnStyle)  # Установка стиля для радиокнопки
            radio_button.setIconSize(QSize(50, 50))  # Устанавливаем размер иконки радиокнопки
            radio_button.setChecked(True)  # По умолчанию выбран последний сервер
            self.radio_buttons.append(radio_button)
            self.layout().addWidget(radio_button)

        # 🔘 Кнопки "Cancel" и "Select Server" с крупным шрифтом
        button_layout = QHBoxLayout()

        cancel_button = QPushButton("Cancel", self)
        cancel_button.setStyleSheet(btnStyle)  # Оформление кнопки Cancel
        cancel_button.setFont(font)
        cancel_button.clicked.connect(self.reject)   # Обработчик нажатия кнопки "Cancel"

        select_server_button = QPushButton("Select Server", self)
        select_server_button.setStyleSheet(btnStyle)  # Оформление кнопки Select Server
        select_server_button.setFont(font)
        select_server_button.clicked.connect(self.select_server)   # Обработчик нажатия кнопки "Select Server"

        button_layout.addWidget(cancel_button)
        button_layout.addWidget(select_server_button)
        self.layout().addLayout(button_layout)

        self.show()


    #def resizeEvent(self, event): # метод resizeEvent будет вызываться при каждом изменении размеров окна, 
    # и размеры QLabel будут обновляться соответствующим образом. 
        #new_size = QSize(self.width() // 2, self.height() // 2)  # Новые размеры
        #self.movie_label.setFixedSize(new_size.scaled(self.width() // 2, self.height() // 2, Qt.AspectRatioMode.KeepAspectRatio))


    def select_server(self):
        # Находим выбранную радиокнопку 
        selected_radio_button = next(radio_button for radio_button in self.radio_buttons if radio_button.isChecked())

        # Получаем информацию о выбранном сервере
        selected_server_name = selected_radio_button.text()  # Получаем имя выбранного сервера 
        selected_server = next((server for server in self.servers if server["name"] == selected_server_name), None)  # Получаем информацию о выбранном сервере

        if selected_server:
            self.selected_server_url = selected_server['url']  # у сервера есть поле 'url'
        else:
            self.selected_server_url = "http://api-serv.ru:8001"  # Значение по умолчанию

        self.accept()  # Закрываем диалоговое окно

    def center(self):
        screen_geometry = QApplication.primaryScreen().geometry()  # Получаем геометрию главного экрана
        window_geometry = self.frameGeometry()  # Получаем геометрию окна
        center_point = screen_geometry.center()  # Находим центр экрана
        window_geometry.moveCenter(center_point)  # Устанавливаем центр окна в центр экрана
        window_geometry.moveTop(window_geometry.top() - 10)  # Добавляем смещение: отодвигаем окно вверх на 10 пикселей
        self.move(window_geometry.topLeft())  # Перемещаем окно
