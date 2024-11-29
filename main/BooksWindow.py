from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QTextBrowser


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
