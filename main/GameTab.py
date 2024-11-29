from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel


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
