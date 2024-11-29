from imports_def import *


class AddWriterWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel("Введите информацию о писателе")
        layout.addWidget(label)
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText("Имя писателя")
        layout.addWidget(self.nameInput)
        self.bookInput = QLineEdit()
        self.bookInput.setPlaceholderText("Название книги")
        layout.addWidget(self.bookInput)
        self.yearInput = QLineEdit()
        self.yearInput.setPlaceholderText("Годы жизни")
        layout.addWidget(self.yearInput)
        button = QPushButton("Добавить писателя")
        button.clicked.connect(self.addWriter)
        layout.addWidget(button)
        self.setLayout(layout)

    def addWriter(self):
        name = self.nameInput.text()
        book = self.bookInput.text()
        year = self.yearInput.text()

        if not name or not book or not year:
            QMessageBox.information(self, "Ошибка", "Введите все поля")
            return

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO writers (name, book, year) VALUES (?, ?, ?)",
                (name, book, year),
            )
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Успешно", "Писатель добавлен!")
            self.close()
        except sqlite3.Error as e:
            QMessageBox.information(
                self, "Ошибка", "Ошибка при работе с базой данных: " + str(e)
            )
