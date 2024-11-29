from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from database import *



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