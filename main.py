import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, \
    QTabWidget, QHBoxLayout, QInputDialog
from PyQt5.QtGui import *
import sqlite3

# Создание базы данных с пользователями
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        email TEXT,
        password TEXT
    )
"""
)

conn.commit()
conn.close()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Литературное путешествие по Воронежу')

        layout = QVBoxLayout()
        label = QLabel('Добро пожаловать!')
        layout.addWidget(label)

        button = QPushButton('Начать работу')
        button.clicked.connect(self.startWork)
        layout.addWidget(button)

        self.setLayout(layout)

    def startWork(self):
        self.authWindow = AuthWindow()
        self.authWindow.show()
        self.close()


class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Авторизация')

        layout = QVBoxLayout()
        label = QLabel('Введите почту и пароль')
        layout.addWidget(label)

        self.emailInput = QLineEdit()
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)

        layout.addWidget(QLabel('Почта'))
        layout.addWidget(self.emailInput)
        layout.addWidget(QLabel('Пароль'))
        layout.addWidget(self.passwordInput)

        buttonLayout = QHBoxLayout()
        loginButton = QPushButton('Войти')
        loginButton.clicked.connect(self.login)
        buttonLayout.addWidget(loginButton)

        registerButton = QPushButton('Авторизация')
        registerButton.clicked.connect(self.register)
        buttonLayout.addWidget(registerButton)

        layout.addLayout(buttonLayout)

        self.setLayout(layout)

    def login(self):
        email = self.emailInput.text()
        password = self.passwordInput.text()

        if not email or not password:
            QMessageBox.information(self, 'Ошибка', 'Введите почту и пароль')
            return

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()

        if user:
            self.mainWindow = MainWindowWithTabs()
            self.mainWindow.show()
            self.close()
        else:
            QMessageBox.information(self, 'Ошибка', 'Неправильная почта или пароль')

    def register(self):
        email = self.emailInput.text()
        password = self.passwordInput.text()

        if not email or not password:
            QMessageBox.information(self, 'Ошибка', 'Введите почту и пароль')
            return
        else:
            self.mainWindow = MainWindowWithTabs()
            self.mainWindow.show()
            self.close()
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        conn.close()
        QMessageBox.information(self, 'Успешно', 'Вы успешно авторизовались!')



class MainWindowWithTabs(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Литературное путешествие по Воронежу')
        layout = QVBoxLayout()
        self.tabWidget = QTabWidget()
        layout.addWidget(self.tabWidget)
        self.mapImage = QLabel()
        self.mapImage.setPixmap(QPixmap('map.png'))
        layout.addWidget(self.mapImage)
        self.setLayout(layout)
        self.quizTab = QuizTab()
        self.tabWidget.addTab(self.quizTab, 'Викторина')
        self.questsTab = QuestsTab()
        self.tabWidget.addTab(self.questsTab, 'Квесты')
        self.gameTab = GameTab()
        self.tabWidget.addTab(self.gameTab, 'Игровой режим')
        self.libraryTab = LibraryTab()
        self.tabWidget.addTab(self.libraryTab, 'Библиотека')
        self.setLayout(layout)


class QuizTab(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel('Викторина')
        layout.addWidget(label)
        button = QPushButton('Начать викторину')
        button.clicked.connect(self.startQuiz)
        layout.addWidget(button)
        self.setLayout(layout)

    def startQuiz(self):
        # реализация викторины
        pass


class QuestsTab(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel('Квесты')
        layout.addWidget(label)
        button = QPushButton('Начать квест')
        button.clicked.connect(self.startQuest)
        layout.addWidget(button)
        self.setLayout(layout)

    def startQuest(self):
        # реализация квестов
        pass


class GameTab(QWidget):
    def init(self):
        super().init()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel('Игровой режим')
        layout.addWidget(label)
        button = QPushButton('Начать игру')
        button.clicked.connect(self.startGame)
        layout.addWidget(button)
        self.setLayout(layout)

    def startGame(self):
        # реализация игрового режима
        pass

class LibraryTab(QWidget):
    def init(self):
        super().init()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel('Библиотека')
        layout.addWidget(label)
        button = QPushButton('Посмотреть книги')
        button.clicked.connect(self.showBooks)
        layout.addWidget(button)
        self.setLayout(layout)

    def showBooks(self):
        # реализация библиотеки
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())