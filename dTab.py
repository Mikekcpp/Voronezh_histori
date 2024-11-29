from imports_def import *


class dTab(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel("Добавить писателя")
        layout.addWidget(label)
        button = QPushButton("Добавить писателя")
        button.clicked.connect(self.startQuest)
        layout.addWidget(button)
        self.setLayout(layout)

    def startQuest(self):
        password, ok = QInputDialog.getText(
            self, "Вход", "Введите пароль администратора"
        )
        if ok and password == "admin":  # замените 'admin' на свой пароль администратора
            self.addWriterWindow = AddWriterWindow()
            self.addWriterWindow.show()
        else:
            QMessageBox.information(
                self, "Ошибка", "Неправильный пароль администратора"
            )
