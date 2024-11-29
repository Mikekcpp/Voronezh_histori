from imports_def import *


class MapTab(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)
        self.mapImage = QLabel()
        self.mapImage.setPixmap(QPixmap("pictures\Карта.png"))
        self.mapImage.resize(self.width(), self.height())  # установите размер картинки
        self.scrollArea.setWidget(self.mapImage)

    def resizeEvent(self, event):
        self.mapImage.resize(self.width(), self.height())
        super().resizeEvent(event)
