from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
                             QMessageBox, QTabWidget, QHBoxLayout, QInputDialog, QScrollArea, QTextBrowser,
                             QTextEdit, QSizePolicy)
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
        self.setWindowTitle('Литературное путешествие по Воронежу')

        self.pImage = QLabel(self)
        self.pImage.setPixmap(QPixmap('приветств.png'))
        self.pImage.setScaledContents(True)  # Масштабирование картинки

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Удаление отступов
        layout.setSpacing(0)  # Удаление расстояния между элементами

        button = QPushButton('Начать работу')
        button.setStyleSheet("background-color: #453530; border-radius: 10px; font-size: 18pt; "
                             "font-weight: bold; color: white;")
        button.clicked.connect(self.startWork)

        layout.addWidget(button)
        layout.setAlignment(button, Qt.AlignCenter)  # Выравнивание кнопки по центру

        self.pImage.setLayout(layout)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.pImage)
        self.layout().setStretchFactor(self.pImage, 1)  # Задаем stretch для картинки

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Обновляем размер картинки при изменении размера окна
        self.pImage.resize(self.width(), self.height())

    def startWork(self):
        self.authWindow = AuthWindow()
        self.authWindow.show()
        self.hide()



class AuthWindow(QWidget):
    MIN_PASSWORD_LENGTH = 6

    def __init__(self):
        super().__init__()

        self.initUI()

    def hash_password(self, password: str) -> str:
        """Хеширует пароль с помощью SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        """Проверяет пароль на длину и содержание"""
        return len(password) >= self.MIN_PASSWORD_LENGTH and '123456' not in password

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Авторизация')

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        layout.setAlignment(Qt.AlignCenter)
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 800, 600)  # Увеличиваем размер картинки
        pixmap = QPixmap('през (3).png')
        self.background.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        label = QLabel('Введите почту и пароль')
        label.setStyleSheet("color: #453530; font-size: 24px;")
        layout.addWidget(label)

        self.emailInput = QLineEdit()
        self.emailInput.setPlaceholderText("Email")
        self.emailInput.setStyleSheet("background-color: rgba(255, 255, 255, 0.5); border-radius: 10px; padding: 10px;")
        self.emailInput.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.emailInput)

        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setPlaceholderText("Пароль")
        self.passwordInput.setStyleSheet("background-color: rgba(255, 255, 255, 0.5); border-radius: 10px; padding: 10px;")
        self.passwordInput.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.passwordInput)

        buttonLayout = QHBoxLayout()
        buttonLayout.setAlignment(Qt.AlignCenter)

        loginButton = QPushButton('Войти')
        loginButton.clicked.connect(self.login)
        loginButton.setStyleSheet("background-color: #453530; color: white; border-radius: 10px; padding: 10px;")
        loginButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        buttonLayout.addWidget(loginButton)

        registerButton = QPushButton('Регистрация')
        registerButton.clicked.connect(self.register)
        registerButton.setStyleSheet("background-color: #453530; color: white; border-radius: 10px; padding: 10px;")
        registerButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        buttonLayout.addWidget(registerButton)

        layout.addLayout(buttonLayout)

    def login(self):
        email = self.emailInput.text()
        password = self.passwordInput.text()

        if not email or not password:
            QMessageBox.information(self, 'Ошибка', 'Введите почту и пароль')
            return
        if '@' not in email:
            QMessageBox.information(self, 'Ошибка', 'Введите корректную почту!')
            return
        if not self.check_password(password):
            QMessageBox.information(self, 'Ошибка', 'Введите корректный пароль! '
                                                    'Пароль должен содержать не меньше 6 символов!')
            return

        hashed_password = self.hash_password(password)

        try:
            with sqlite3.connect("users.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, hashed_password))
                user = cursor.fetchone()

                if user:
                    self.mainWindow = MainWindowWithTabs()
                    self.mainWindow.show()
                    self.hide()
                else:
                    QMessageBox.information(self, 'Ошибка', 'Неправильная почта или пароль')
        except sqlite3.Error as e:
            QMessageBox.information(self, 'Ошибка', 'Ошибка при работе с базой данных: ' + str(e))

    def register(self):
        email = self.emailInput.text()
        password = self.passwordInput.text()

        if not email or not password:
            QMessageBox.information(self, 'Ошибка', 'Введите почту и пароль')
            return
        if '@' not in email:
            QMessageBox.information(self, 'Ошибка', 'Введите корректную почту!')
            return
        if not self.check_password(password):
            QMessageBox.information(self, 'Ошибка', 'Введите корректный пароль! '
                                                    'Пароль должен содержать не меньше 6 символов!')
            return

        try:
            with sqlite3.connect("users.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
                user = cursor.fetchone()

                if user:
                    QMessageBox.information(self, 'Ошибка', 'Пользователь с таким email уже существует')
                    return

                hashed_password = self.hash_password(password)
                cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
                conn.commit()
                QMessageBox.information(self, 'Успешно', 'Вы успешно зарегистрировались!')
                self.close()
                self.mainWindow = MainWindowWithTabs()
                self.mainWindow.show()
                self.hide()
        except sqlite3.Error as e:
            QMessageBox.information(self, 'Ошибка', 'Ошибка при работе с базой данных: ' + str(e))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background.resize(self.size())
        pixmap = QPixmap('photo_5355309471032797434_y.jpg')
        self.background.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))





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
            with open(file_name, 'r', encoding='utf-8') as file:
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
        self.mapImage.setPixmap(QPixmap('през (2).png'))
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
            self.scoreLabel.setText('Литеробаллы: ' + str(self.score))
            QMessageBox.information(self, 'Правильный код!', f'Вы свои литеробаллы!')
        else:
            QMessageBox.information(self, 'Ошибка', 'Код неверный или уже использован!')

    def resizeEvent(self, event):
        super().resizeEvent(event)


class dTab(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Фоновое изображение
        self.background_image = QLabel(self)
        self.background_image.setStyleSheet("border: none;")
        self.background_image.setScaledContents(True)
        self.background_image.setPixmap(QPixmap("през перо.png"))  # Путь к картинке
        self.background_image.resize(self.width(), self.height())  # Размеры окна

        # Заголовок
        self.label = QLabel('Добавить писателя', self)
        self.label.setStyleSheet("color: white; font-size: 24pt;")
        self.label.move(350, 250)

        # Кнопка "Добавить писателя"
        self.button = QPushButton('Добавить писателя', self)
        self.button.setStyleSheet(
            "background-color: #453530; color: white; border: none; border-radius: 10px; padding: 15px; font-size: 16pt;")
        self.button.clicked.connect(self.startQuest)

        # Автоматическая настройка размера кнопки
        self.button.setFixedSize(250, 60)  # Увеличиваем размеры кнопки
        self.button.move(self.width() // 2 - self.button.width() // 2, self.height() - self.button.height() - 20)

        # Поднимаем элементы на передний план
        self.background_image.raise_()
        self.label.raise_()
        self.button.raise_()

    def resizeEvent(self, event):
        # Изменяем размеры фона
        self.background_image.resize(self.width(), self.height())
        # Центрируем заголовок
        self.label.move(self.width() // 2 - self.label.width() // 2, self.height() // 2 - self.label.height() // 2)
        # Перемещаем кнопку
        self.button.move(self.width() // 2 - self.button.width() // 2, self.height() - self.button.height() - 20)
        super().resizeEvent(event)

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
        # Устанавливаем размеры окна
        self.setMinimumSize(800, 600)

        # Фоновое изображение
        self.background_image = QLabel(self)
        self.background_image.setStyleSheet("border: none;")
        self.background_image.setScaledContents(True)
        self.background_image.setPixmap(QPixmap("през перо.png"))  # Путь к картинке

        main_layout = QVBoxLayout(self)

        # Центрируем заголовок
        # Центрируем заголовок
        label = QLabel('Писатели', self)
        label.setStyleSheet("color: white; font-size: 24pt;")
        label.setAlignment(Qt.AlignCenter)  # Центрируем текст
        main_layout.addWidget(label, stretch=1, alignment=Qt.AlignHCenter)

        # Добавляем растяжение для центрирования заголовка по вертикали
        main_layout.addStretch()

        # Вертикальный компоновщик для кнопок
        button_layout = QHBoxLayout()

        button_all = QPushButton('Воронежские писатели', self)
        button_all.setStyleSheet("background-color: #453530; color: white; border: none; border-radius: "
                                 "10px; padding: 10px; font-size: 16pt;")  # Уменьшаем размер кнопки
        button_all.setFixedSize(250, 60)  # Устанавливаем фиксированный размер кнопки
        button_all.clicked.connect(self.showAllWriters)
        button_layout.addWidget(button_all, alignment=Qt.AlignCenter)  # Центрируем кнопку

        button_added = QPushButton('Добавленные писатели', self)
        button_added.setStyleSheet("background-color: #453530; color: white; border: none; border-radius: "
                                   "10px; padding: 10px; font-size: 16pt;")  # Уменьшаем размер кнопки
        button_added.setFixedSize(250, 60)  # Устанавливаем фиксированный размер кнопки
        button_added.clicked.connect(self.showAddedWriters)
        button_layout.addWidget(button_added, alignment=Qt.AlignCenter)  # Центрируем кнопку

        # Уменьшаем расстояние между кнопками
        button_layout.setSpacing(20)  # Устанавливаем расстояние между кнопками

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def resizeEvent(self, event):
        self.background_image.resize(self.size())
        super().resizeEvent(event)

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
        # Set the background color of the LibraryTab
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))  # Light gray background
        self.setPalette(palette)

        layout = QVBoxLayout()
        label = QLabel('Библиотека')
        layout.addWidget(label)

        # Create buttons with a style
        button_style = """
            QPushButton {
                background-color: #453530;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #453530;  /* Darker brown on hover */
            }
        """

        button = QPushButton('Посмотреть добавленные книги')
        button.setStyleSheet(button_style)
        button.clicked.connect(self.showBooks)
        layout.addWidget(button)

        button = QPushButton('Посмотреть книги, с возможностью покупки')
        button.setStyleSheet(button_style)
        button.clicked.connect(self.showBooks_d)
        layout.addWidget(button)

        button = QPushButton('Добавить книгу')
        button.setStyleSheet(button_style)
        button.clicked.connect(self.addBook)
        layout.addWidget(button)

        self.booksText = QTextBrowser()
        # Set a background pixmap for the QTextBrowser
        self.booksText.setStyleSheet("background-image: url('през перо.png');")  # Set your image path here
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
