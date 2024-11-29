from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
                             QMessageBox, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
import sqlite3


class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 350, 250)  # Увеличиваем размер окна
        self.setFixedSize(350, 250)  # Делаем окно не растягиваемым
        self.setWindowTitle('Авторизация')

        # Добавляем картинку на фоне
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 350, 250)  # Увеличиваем размер картинки
        pixmap = QPixmap('1.jpg')
        pixmap = pixmap.scaled(450, 350, Qt.KeepAspectRatio)  # Увеличиваем размер картинки
        self.background.setPixmap(pixmap)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Добавляем отступы

        label = QLabel('Введите почту и пароль')
        label.setStyleSheet("color: #453530;")  # Делаем надпись коричневой
        layout.addWidget(label)

        # Добавляем надписи в поле ввода
        self.emailInput = QLineEdit()
        self.emailInput.setPlaceholderText("Email")
        self.emailInput.setStyleSheet("background-color: rgba(255, 255, 255, 0.5); border-radius: 10px; padding: 5px;")
        layout.addWidget(self.emailInput)

        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setPlaceholderText("Пароль")
        self.passwordInput.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.5); border-radius: 10px; padding: 5px;")
        layout.addWidget(self.passwordInput)

        buttonLayout = QHBoxLayout()
        loginButton = QPushButton('Войти')
        loginButton.clicked.connect(self.login)
        loginButton.setStyleSheet("background-color: #453530; color: white; border-radius: 10px; padding: 5px;")
        buttonLayout.addWidget(loginButton)

        registerButton = QPushButton('Регистрация')
        registerButton.clicked.connect(self.register)
        registerButton.setStyleSheet("background-color: #453530; color: white; border-radius: 10px; padding: 5px;")
        buttonLayout.addWidget(registerButton)

        layout.addLayout(buttonLayout)

        container = QWidget(self)
        container.setGeometry(0, 0, 350, 250)
        container.setLayout(layout)
        container.setStyleSheet("background-color: transparent;")  # Делаем контейнер прозрачным

        self.background.lower()  # Перемещаем картинку на задний план
        container.raise_()  # Перемещаем контейнер на передний план

    def login(self):
        email = self.emailInput.text()
        password = self.passwordInput.text()

        if not email or not password:
            QMessageBox.information(self, 'Ошибка', 'Введите почту и пароль')
            return
        if '@' not in email:
            QMessageBox.information(self, 'Ошибка', 'Введите корректную почту!')
            return
        if len(password) < 6 or '123456' in password:
            QMessageBox.information(self, 'Ошибка', 'Введите корректный пароль! '
                                                    'Пароль должен содержать не меньше 6 символов!')
            return

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()

        if user:
            self.mainWindow = MainWindowWithTabs()
            self.mainWindow.quizWindow.userId = user[0]  # сохраните ID пользователя
            self.mainWindow.show()
            self.hide()
        else:
            QMessageBox.information(self, 'Ошибка', 'Неправильная почта или пароль')
        conn.close()

    def register(self):
        email = self.emailInput.text()
        password = self.passwordInput.text()

        if not email or not password:
            QMessageBox.information(self, 'Ошибка', 'Введите почту и пароль')
            return
        if '@' not in email:
            QMessageBox.information(self, 'Ошибка', 'Введите корректную почту!')
            return
        if len(password) < 6 or '123456' in password:
            QMessageBox.information(self, 'Ошибка', 'Введите корректный пароль! '
                                                    'Пароль должен содержать не меньше 6 символов!')
            return

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))

            user = cursor.fetchone()

            if user:
                QMessageBox.information(self, 'Ошибка', 'Пользователь с таким email уже существует')
                conn.close()
                return

            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
            conn.close()
            QMessageBox.information(self, 'Успешно', 'Вы успешно зарегистрировались!')
            self.close()
            self.mainWindow = MainWindowWithTabs()
            self.mainWindow.show()

        except sqlite3.Error as e:
            QMessageBox.information(self, 'Ошибка', 'Ошибка при работе с базой данных: ' + str(e))
