from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
                             QMessageBox, QTabWidget, QHBoxLayout, QInputDialog, QScrollArea, QTextBrowser)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
import sqlite3, sys
import random

from database import *

# Создание базы данных с пользователями и вопросами
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute(
    '''  
        CREATE TABLE IF NOT EXISTS writers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            book TEXT,
            year INTEGER
        )
    ''')

cursor.execute(
    '''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        email TEXT,
        password TEXT,
        score INTEGER
    )''')

cursor.execute(
    ''' DROP TABLE IF EXISTS questions'''
)

cursor.execute(
    '''CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY,
        question TEXT,
        answer TEXT,
        difficulty INTEGER,
        score INTEGER
    )''')

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


class MainWindowWithTabs(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 400, 300)  # установите начальный размер окна
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
        self.show()


class MapTab(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)
        self.mapImage = QLabel()
        self.mapImage.setPixmap(QPixmap('Карта.png'))
        self.mapImage.resize(self.width(), self.height())  # установите размер картинки
        self.scrollArea.setWidget(self.mapImage)

    def resizeEvent(self, event):
        self.mapImage.resize(self.width(), self.height())
        super().resizeEvent(event)


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
        self.userId = None  # добавьте переменную для хранения ID пользователя

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
        if self.questions:
            self.showQuestion()
        else:
            self.questionLabel.setText('Вопросов нет!')

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
                self.updateScore()  # обновите значение score в базе данных
                QMessageBox.information(self, 'Правильно!', 'Вы правильно ответили на вопрос!')
            else:
                QMessageBox.information(self, 'Неправильно!', 'Вы неправильно ответили на вопрос!')
            self.currentQuestion += 1
            self.answerInput.clear()
            self.showQuestion()
        else:
            self.questionLabel.setText('Викторина окончена!')
            self.answerInput.setReadOnly(True)

    def updateScore(self):
        if self.userId is not None:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET score = ? WHERE id = ?", (self.score, self.userId))
            conn.commit()
            conn.close()
        else:
            print("ID пользователя не задан")

    def updateScore(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET score = ? WHERE id = ?", (self.score, self.userId))
        conn.commit()
        conn.close()


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
        self.bookInput.setPlaceholderText('Название книги')
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
        button = QPushButton('Посмотреть добавленные книги')
        button.clicked.connect(self.showBooks)
        layout.addWidget(button)
        button = QPushButton('Посмотреть книги, с возможностью покупки')
        button.clicked.connect(self.showBooks_d)
        layout.addWidget(button)
        button = QPushButton('Добавить книгу')
        button.clicked.connect(self.addBook)
        layout.addWidget(button)
        self.booksText = QTextBrowser()
        layout.addWidget(self.booksText)
        self.setLayout(layout)

    def showBooks(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, book FROM writers")
        books = cursor.fetchall()
        conn.close()

        text = ""
        for book in books:
            text += f"Автор: {book[0]}\nКнига: {book[1]}\n\n"

        self.booksText.setText(text)

        text = ""
        for book in books:
            text += f"Автор: {book[0]}\nКнига: {book[1]}\n\n"

        self.booksText.setText(text)

    def showBooks_d(self):
        self.booksWindow = BooksWindow()
        self.booksWindow.show()

    def addBook(self):
        password, ok = QInputDialog.getText(self, 'Вход', 'Введите пароль администратора')
        if ok and password == 'admin1':  # замените 'admin' на свой пароль администратора
            self.addBookWindow = AddBookWindow()
            self.addBookWindow.show()
        else:
            QMessageBox.information(self, 'Ошибка', 'Неправильный пароль администратора')


class AddBookWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel('Введите информацию о книге')
        layout.addWidget(label)
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText('Автор')
        layout.addWidget(self.nameInput)
        self.bookInput = QLineEdit()
        self.bookInput.setPlaceholderText('Название книги')
        layout.addWidget(self.bookInput)
        button = QPushButton('Добавить книгу')
        button.clicked.connect(self.addBook)
        layout.addWidget(button)
        self.setLayout(layout)

    def addBook(self):
        name = self.nameInput.text()
        book = self.bookInput.text()

        if not name or not book:
            QMessageBox.information(self, 'Ошибка', 'Введите все поля')
            return

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO writers (name, book) VALUES (?, ?)", (name, book))
            conn.commit()
            conn.close()
            QMessageBox.information(self, 'Успешно', 'Книга добавлена!')
            self.close()
        except sqlite3.Error as e:
            QMessageBox.information(self, 'Ошибка', 'Ошибка при работе с базой данных: ' + str(e))


class BooksWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.booksText = QTextBrowser()
        layout.addWidget(self.booksText)
        button = QPushButton('Закрыть')
        button.clicked.connect(self.close)
        layout.addWidget(button)
        self.setLayout(layout)

        try:
            with open('books.txt', 'r', encoding='utf-8') as file:
                text = file.read()
                self.booksText.setText(text)
        except FileNotFoundError:
            QMessageBox.information(self, 'Ошибка', 'Файл books.txt не найден')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
