from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel


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
