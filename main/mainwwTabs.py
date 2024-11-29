from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget


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
        self.quizTab = QuizTab()
        self.tabWidget.addTab(self.quizTab, 'Викторина')
        self.dTab = dTab()
        self.tabWidget.addTab(self.dTab, 'Добавить писателя')
        self.gameTab = GameTab()
        self.tabWidget.addTab(self.gameTab, 'Писатели')
        self.libraryTab = LibraryTab()
        self.tabWidget.addTab(self.libraryTab, 'Библиотека')
        self.mapTab = MapTab()
        self.tabWidget.addTab(self.mapTab, 'Карта')
        self.show()
