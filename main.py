from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
                             QMessageBox, QTabWidget, QHBoxLayout, QInputDialog, QScrollArea, QTextBrowser, QTextEdit)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sqlite3, sys
import hashlib

password = 'admin'
hashed_password = hashlib.sha256(password.encode()).hexdigest()
print(hashed_password)
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
    '''CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY,
        question TEXT,
        answer TEXT,
        score INTEGER
    )''')

cursor.execute(
    '''CREATE TABLE IF NOT EXISTS user_scores (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        score INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')

# Добавление вопросов в базу данных
questions = [
    ("Кто написал роман 'Война и мир'?", "Лев Толстой", 1),
    ("Кто написал роман 'Преступление и наказание'?", "Федор Достоевский", 2),
    ("Кто написал роман 'Анна Каренина'?", "Лев Толстой", 1),
    ("Кто написал роман 'Братья Карамазовы'?", "Федор Достоевский", 3),
    ("Кто написал роман 'Воскресение'?", "Лев Толстой", 1),
]

for question, answer, score in questions:
    cursor.execute("INSERT OR IGNORE INTO questions (question, answer, score) VALUES (?, ?, ?)",
                   (question, answer, score))

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

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def initUI(self):
        self.setGeometry(300, 300, 350, 250)  # Увеличиваем размер окна
        self.setFixedSize(350, 250)  # Делаем окно не растягиваемым
        self.setWindowTitle('Авторизация')

        # Добавляем картинку на фоне
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 350, 250)  # Увеличиваем размер картинки
        pixmap = QPixmap('photo_5355309471032797434_y.jpg')
        pixmap = pixmap.scaled(450, 350, Qt.KeepAspectRatio)  # Увеличиваем размер картинки
        self.background.setPixmap(pixmap)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
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

        hashed_password = self.hash_password(password)

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, hashed_password))
        user = cursor.fetchone()

        if user:
            if user:
                # Передаем userId в MainWindowWithTabs
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

            hashed_password = self.hash_password(password)
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email,
                                                                                 hashed_password))
            conn.commit()
            conn.close()
            QMessageBox.information(self, 'Успешно', 'Вы успешно зарегистрировались!')
            self.close()
            self.mainWindow = MainWindowWithTabs()
            self.mainWindow.show()
            self.hide()

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
        self.dTab = dTab()
        self.tabWidget.addTab(self.dTab, 'Добавить писателя')
        self.gameTab = GameTab()
        self.tabWidget.addTab(self.gameTab, 'Писатели')
        self.libraryTab = LibraryTab()
        self.tabWidget.addTab(self.libraryTab, 'Библиотека')
        self.mapTab = MapTab()
        self.tabWidget.addTab(self.mapTab, 'Карта')
        self.show()

    def updateScore(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT score FROM users WHERE id = ?", (self.userId,))
        score = cursor.fetchone()
        conn.close()
        if score is not None:
            self.scoreLabel.setText('Баллы: ' + str(score[0]))


class FixedButton(QLabel):
    def __init__(self, x, y, parent=None, point_number=None):
        super().__init__(parent)
        self.setGeometry(x, y, 20, 20)
        self.setStyleSheet(
            "background-color: transparent; border: 2px solid #964B00; border-radius: 10px")
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.point_number = point_number
        self.x = x
        self.y = y

    def enterEvent(self, event):
        self.setStyleSheet(
            "background-color: transparent; border: 2px solid #FFD700; border-radius: 10px")

    def leaveEvent(self, event):
        self.setStyleSheet(
            "background-color: transparent; border: 2px solid #964B00; border-radius: 10px")

    def mousePressEvent(self, event):
        if self.point_number is not None:
            self.window = PointWindow(self.point_number)
            self.window.show()


class PointWindow(QWidget):
    def __init__(self, point_number):
        super().__init__()
        self.point_number = point_number
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        file_name = f"point_{self.point_number}.txt"
        try:
            with open(file_name, 'r', encoding='utf-8') as file:  # Убедитесь, что используете правильную кодировку
                text = file.read()
                self.text_edit = QTextEdit()
                self.text_edit.setText(text)
                self.text_edit.setReadOnly(True)
                layout.addWidget(self.text_edit)
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл {file_name} не найден.")
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {str(e)}")
            self.close()


class MapTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.codes = ["CODE1", "CODE2", "CODE3", "CODE4", "CODE5",
                      "CODE6", "CODE7", "CODE8", "CODE9", "CODE10",
                      "CODE11", "CODE12", "CODE13", "CODE14", "CODE15",
                      "CODE16", "CODE17", "CODE18"]  # Заданные коды
        self.user_answers = {code: False for code in self.codes}
        self.score = 0

    def initUI(self):
        layout = QVBoxLayout()
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)

        self.mapImage = QLabel()
        self.mapImage.setPixmap(QPixmap('Карта.png'))
        self.mapImage.setScaledContents(True)
        self.scrollArea.setWidget(self.mapImage)

        self.create_buttons()

        self.codeInput = QLineEdit()
        self.codeInput.setPlaceholderText("Введите код")
        layout.addWidget(self.codeInput)

        self.checkCodeButton = QPushButton('Проверить код')
        self.checkCodeButton.clicked.connect(self.checkCode)
        layout.addWidget(self.checkCodeButton)

        self.scoreLabel = QLabel('Баллы: 0')
        layout.addWidget(self.scoreLabel)

    def create_buttons(self):
        coordinates = [(560, 50), (727, 67), (597, 141), (465, 252), (1098, 328),
                       (927, 417), (1343, 403), (1010, 484), (1212, 475), (943, 561),
                       (405, 604), (620, 711), (1273, 688), (965, 912), (590, 955),
                       (880, 955), (790, 1038), (965, 1023)]

        for i, (x, y) in enumerate(coordinates):
            button = FixedButton(x, y, self.mapImage, i)
            button.show()

    def checkCode(self):
        code = self.codeInput.text()
        if code in self.codes and not self.user_answers[code]:
            self.score += 10
            self.user_answers[code] = True
            self.scoreLabel.setText('Баллы: ' + str(self.score))
            QMessageBox.information(self, 'Правильный код!', f'Вы ввели правильный код: {code}!')
        else:
            QMessageBox.information(self, 'Ошибка', 'Код неверный или уже использован!')

    def resizeEvent(self, event):
        super().resizeEvent(event)



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
        if ok and hashlib.sha256(password.encode()).hexdigest() == ('8c6976e5b5410415bde908bd4dee15dfb167a9c8'
                                                                    '73fc4bb8a81f6f2ab448a918'):
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
            cursor.execute("INSERT INTO writers (name, book, year) VALUES (?, ?, ?)", (name,
                                                                                       book, year))
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
        button.clicked.connect(self.showAllWriters)
        layout.addWidget(button)
        button = QPushButton('Добавленные писатели')
        button.clicked.connect(self.showAddedWriters)
        layout.addWidget(button)
        self.setLayout(layout)

    def showAllWriters(self):
        self.allWritersWindow = AllWritersWindow()
        self.allWritersWindow.show()

    def showAddedWriters(self):
        self.addedWritersWindow = AddedWritersWindow()
        self.addedWritersWindow.show()


class AllWritersWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.writersText = QTextBrowser()
        layout.addWidget(self.writersText)
        button = QPushButton('Закрыть')
        button.clicked.connect(self.close)
        layout.addWidget(button)
        self.setLayout(layout)
        try:
            with open('writers.txt', 'r', encoding='utf-8') as file:
                text = file.read()
                self.writersText.setText(text)
        except FileNotFoundError:
            QMessageBox.information(self, 'Ошибка', 'Файл не найден')


class AddedWritersWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.writersText = QTextBrowser()
        layout.addWidget(self.writersText)
        button = QPushButton('Закрыть')
        button.clicked.connect(self.close)
        layout.addWidget(button)
        self.setLayout(layout)
        self.showWriters()

    def showWriters(self):
        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("SELECT name, book, year FROM writers")
            writers = cursor.fetchall()
            conn.close()

            text = ""
            for writer in writers:
                text += f"Имя: {writer[0]}\nКнига: {writer[1]}\nГоды жизни: {writer[2]}\n\n"

            self.writersText.setText(text)
        except sqlite3.Error as e:
            QMessageBox.information(self, 'Ошибка', 'Ошибка при работе с базой данных: ' + str(e))


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

    def showBooks_d(self):
        self.booksWindow = BooksWindow()
        self.booksWindow.show()

    def addBook(self):
        password, ok = QInputDialog.getText(self, 'Вход', 'Введите пароль администратора')
        if ok and hashlib.sha256(password.encode()).hexdigest() == ('8c6976e5b5410415bde908bd4dee'
                                                                    '15dfb167a9c873fc4bb8a81f6f2ab448a918'):
            self.AddBookWindow = AddBookWindow()
            self.AddBookWindow.show()
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
    sys.exit(app.exec())
