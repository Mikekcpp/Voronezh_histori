from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 800, 600)  # Установка размера окна
        self.setFixedSize(800, 600)  # Установка неподвижного размера окна
        self.setWindowTitle('Литературное путешествие по Воронежу')

        self.pImage = QLabel(self)
        self.pImage.setPixmap(QPixmap('приветств.png'))
        self.pImage.setScaledContents(True)  # Масштабирование картинки
        self.pImage.resize(800, 600)  # Установка размера картинки

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Удаление отступов
        layout.setSpacing(0)  # Удаление расстояния между элементами

        self.pImage.setLayout(layout)

        button = QPushButton('Начать работу')
        button.setFixedSize(200, 50)  # Установка размера кнопки
        button.setStyleSheet("background-color: #453530; border-radius: 10px; font-size: 18pt; "
                             "font-weight: bold; color: white;")
        button.clicked.connect(self.startWork)

        layout.addWidget(button)
        layout.setAlignment(button, Qt.AlignCenter)  # Выравнивание кнопки по центру

        self.setLayout(layout)

    def startWork(self):
        self.authWindow = AuthWindow()
        self.authWindow.show()
        self.hide()
