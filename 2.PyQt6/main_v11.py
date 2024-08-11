# python main_v11.py

import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QFileDialog, QWidget, QHBoxLayout, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap

def format_file_size(size_in_bytes):
    # size_in_bytes должно быть числом (размером файла в байтах)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} TB"

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Настройка основного окна
        self.setWindowTitle("X-Rays Model HQ-SAM App [v11, 2023]")
        self.setGeometry(100, 100, 600, 800)
        self.center()

        # Оформление виджетов
        borderStyle = """
        border: 2px solid darkviolet;
        border-radius: 5px;
        margin: 1px;
        border: 2px solid white;
        """

        btnStyle = f"""
        QPushButton {{
            background-color: darkgreen;
            padding: 10px;
            color: white;
            font-size: 14px;
            {borderStyle}
        }}
        QPushButton:hover {{
            background-color: limegreen;
        }}
        """

        # Создание виджетов
        centralWidget = QWidget(self)
        mainLayout = QVBoxLayout()

        # Виджет для изображения
        self.imageLabel = QLabel(self) # Создание виджета QLabel
        self.imageLabel.setFixedSize(596, 660)  # Установка размеров для виджета изображений
        self.imageLabel.setStyleSheet(borderStyle)
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Выравнивание изображения по центру виджета
        self.imageLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Позволяет QLabel растягиваться

        # Виджет для вывода информации
        self.infoLabel = QLabel("Выберите изображение", self)
        self.infoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Выравнивание изображения по центру виджета

        # Центрирование виджета изображения
        imageLayout = QHBoxLayout()
        imageLayout.addStretch(1)  # Эти растягивания обеспечивают центрирование виджета с изображением
        mainLayout.addLayout(imageLayout, 8)  # 8 частей из 9 для виджета изображения
        mainLayout.addWidget(self.infoLabel, 1)  # 1 часть из 9 для виджета с информацией

        # создание и добавление кнопок 
        btnLoad = QPushButton("IMAGE LOAD", self)
        btnLoad.clicked.connect(self.loadImage)
        btnLoad.setStyleSheet(btnStyle)

        btnPredict = QPushButton("PREDICT", self)
        btnPredict.setStyleSheet(btnStyle)

        btnSave = QPushButton("SAVE", self)
        btnSave.setStyleSheet(btnStyle)

        btnTelegram = QPushButton("-> Telegram", self)
        btnTelegram.setStyleSheet(btnStyle)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(btnLoad)
        buttonLayout.addWidget(btnPredict)
        buttonLayout.addWidget(btnSave)
        buttonLayout.addWidget(btnTelegram)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
