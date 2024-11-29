from imports_def import *


class AddBookWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel("Введите информацию о книге")
        layout.addWidget(label)
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText("Автор")
        layout.addWidget(self.nameInput)
        self.bookInput = QLineEdit()
        self.bookInput.setPlaceholderText("Название книги")
        layout.addWidget(self.bookInput)
        button = QPushButton("Добавить книгу")
        button.clicked.connect(self.addBook)
        layout.addWidget(button)
        self.setLayout(layout)

    def addBook(self):
        name = self.nameInput.text()
        book = self.bookInput.text()

        if not name or not book:
            QMessageBox.information(self, "Ошибка", "Введите все поля")
            return

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO writers (name, book) VALUES (?, ?)", (name, book)
            )
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Успешно", "Книга добавлена!")
            self.close()
        except sqlite3.Error as e:
            QMessageBox.information(
                self, "Ошибка", "Ошибка при работе с базой данных: " + str(e)
            )
