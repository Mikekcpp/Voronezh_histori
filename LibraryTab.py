from imports_def import *

from database import *
from BooksWindow import *
from AddBookWindow import *


class LibraryTab(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel("Библиотека")
        layout.addWidget(label)
        button = QPushButton("Посмотреть добавленные книги")
        button.clicked.connect(self.showBooks)
        layout.addWidget(button)
        button = QPushButton("Посмотреть книги, с возможностью покупки")
        button.clicked.connect(self.showBooks_d)
        layout.addWidget(button)
        button = QPushButton("Добавить книгу")
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
        password, ok = QInputDialog.getText(
            self, "Вход", "Введите пароль администратора"
        )
        if (
            ok and password == "admin1"
        ):  # замените 'admin' на свой пароль администратора
            self.addBookWindow = AddBookWindow()
            self.addBookWindow.show()
        else:
            QMessageBox.information(
                self, "Ошибка", "Неправильный пароль администратора"
            )
