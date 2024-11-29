import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, \
    QTabWidget, QHBoxLayout, QInputDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
import random

# Создание базы данных с пользователями и вопросами
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS writers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        book TEXT,
        year INTEGER
    )
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        email TEXT,
        password TEXT,
        score INTEGER
    )
"""
)

cursor.execute(
    """
    DROP TABLE IF EXISTS questions
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY,
        question TEXT,
        answer TEXT,
        difficulty INTEGER,
        score INTEGER
    )
"""
)


# Добавление вопросов в базу данных
questions = [
    ("Кто написал роман 'Война и мир'?", "Лев Толстой", 1, 10),
    ("Кто написал роман 'Преступление и наказание'?", "Федор Достоевский", 1, 10),
    ("Кто написал роман 'Анна Каренина'?", "Лев Толстой", 1, 10),
    ("Кто написал роман 'Братья Карамазовы'?", "Федор Достоевский", 1, 10),
    ("Кто написал роман 'Воскресение'?", "Лев Толстой", 1, 10),
    # Добавьте еще вопросы...
]

for question, answer, difficulty, score in questions:
    cursor.execute("INSERT OR IGNORE INTO questions (question, answer, difficulty, score) VALUES (?, ?, ?, ?)",
                   (question, answer, difficulty, score))


conn.commit()
conn.close()


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

        registerButton = QPushButton('Регистрация')
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
        if 'gmail.com' not in email or 'yandex.ru' not in email:
            QMessageBox.information(self, 'Ошибка', 'Введите корректную почту!')
            return
        if len(password) < 6:
            QMessageBox.information(self, 'Ошибка', 'Введите корректный пароль! '
                                                    'Пароль должен содержать не меньше 6 символов!')
            return


        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()

        if user:
            self.mainWindow = MainWindowWithTabs()
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
        if 'gmail.com' not in email or 'yandex.ru' not in email:
            QMessageBox.information(self, 'Ошибка', 'Введите корректную почту!')
            return
        if len(password) < 6:
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

class MainWindowWithTabs(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 400, 300)  # измените размер окна
        self.setWindowTitle('Литературное путешествие по Воронежу')
        layout = QVBoxLayout()
        self.tabWidget = QTabWidget()
        layout.addWidget(self.tabWidget)
        self.setLayout(layout)
        self.quizTab = QuizTab()
        self.tabWidget.addTab(self.quizTab, 'Викторина')
        self.dTab = dTab()
        self.tabWidget.addTab(self.dTab, 'Добавить писателя')
        self.gameTab = GameTab()
        self.tabWidget.addTab(self.gameTab, 'Писатели')
        self.libraryTab = LibraryTab()
        self.tabWidget.addTab(self.libraryTab, 'Библиотека')
        self.mapTab = MapTab()
        self.tabWidget.addTab(self.mapTab, 'Карта')



class MapTab(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.mapImage = QLabel()
        self.mapImage.setPixmap(QPixmap('Карта.png'))
        layout.addWidget(self.mapImage)
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
        self.quizWindow = QuizWindow()
        self.quizWindow.show()


class QuizWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.score = 0
        self.currentQuestion = 0
        self.questions = self.getQuestions()

    def initUI(self):
        layout = QVBoxLayout()
        self.questionLabel = QLabel()
        layout.addWidget(self.questionLabel)
        self.answerInput = QLineEdit()
        layout.addWidget(self.answerInput)
        button = QPushButton('Ответить')
        button.clicked.connect(self.checkAnswer)
        layout.addWidget(button)
        self.scoreLabel = QLabel('Счет: 0')
        layout.addWidget(self.scoreLabel)
        self.setLayout(layout)
        self.showQuestion()

    def getQuestions(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions")
        questions = cursor.fetchall()
        conn.close()
        return questions

    def showQuestion(self):
        if self.currentQuestion < len(self.questions):
            question = self.questions[self.currentQuestion]
            self.questionLabel.setText(question[1])
        else:
            self.questionLabel.setText('Викторина окончена!')
            self.answerInput.setReadOnly(True)

    def checkAnswer(self):
        if self.currentQuestion < len(self.questions):
            question = self.questions[self.currentQuestion]
            answer = self.answerInput.text()
            if answer.lower() == question[2].lower():
                self.score += question[4]
                self.scoreLabel.setText('Счет: ' + str(self.score))
                QMessageBox.information(self, 'Правильно!', 'Вы правильно ответили на вопрос!')
            else:
                QMessageBox.information(self, 'Неправильно!', 'Вы неправильно ответили на вопрос!')
            self.currentQuestion += 1
            self.answerInput.clear()
            self.showQuestion()
        else:
            self.questionLabel.setText('Викторина окончена!')
            self.answerInput.setReadOnly(True)


class dTab(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel('Добавить писателя')
        layout.addWidget(label)
        button = QPushButton('Добавить писателя')
        button.clicked.connect(self.startQuest)
        layout.addWidget(button)
        self.setLayout(layout)

    def startQuest(self):
        password, ok = QInputDialog.getText(self, 'Вход', 'Введите пароль администратора')
        if ok and password == 'admin':  # замените 'admin' на свой пароль администратора
            self.addWriterWindow = AddWriterWindow()
            self.addWriterWindow.show()
        else:
            QMessageBox.information(self, 'Ошибка', 'Неправильный пароль администратора')

class AddWriterWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel('Введите информацию о писателе')
        layout.addWidget(label)
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText('Имя писателя')
        layout.addWidget(self.nameInput)
        self.bookInput = QLineEdit()
        self.bookInput.setPlaceholderText('Название книг')
        layout.addWidget(self.bookInput)
        self.yearInput = QLineEdit()
        self.yearInput.setPlaceholderText('Годы жизни')
        layout.addWidget(self.yearInput)
        button = QPushButton('Добавить писателя')
        button.clicked.connect(self.addWriter)
        layout.addWidget(button)
        self.setLayout(layout)

    def addWriter(self):
        name = self.nameInput.text()
        book = self.bookInput.text()
        year = self.yearInput.text()

        if not name or not book or not year:
            QMessageBox.information(self, 'Ошибка', 'Введите все поля')
            return

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO writers (name, book, year) VALUES (?, ?, ?)", (name, book, year))
            conn.commit()
            conn.close()
            QMessageBox.information(self, 'Успешно', 'Писатель добавлен!')
            self.close()
        except sqlite3.Error as e:
            QMessageBox.information(self, 'Ошибка', 'Ошибка при работе с базой данных: ' + str(e))


class GameTab(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel('Писатели')
        layout.addWidget(label)
        button = QPushButton('Все наши писатели')
        button.clicked.connect(self.startGame)
        layout.addWidget(button)
        self.setLayout(layout)

    def startGame(self):
        # реализация игрового режима
        pass


class LibraryTab(QWidget):
    def __init__(self):
        super().__init__()

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