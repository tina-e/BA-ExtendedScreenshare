import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter, QPen

class Area(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width = 750
        self.window_height = 500
        self.border_width = 5
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.pix = QPixmap(self.rect().size())
        self.pix.fill(Qt.white)

        self.begin, self.destination = QPoint(1, 1), QPoint(self.window_width-self.border_width+1, self.window_height-self.border_width+1)


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(0.8)
        painter.drawPixmap(QPoint(), self.pix)
        if not self.begin.isNull() and not self.destination.isNull():
            pen = QPen(Qt.red, self.border_width)
            painter.setPen(pen)
            rect = QRect(self.begin, self.destination)
            painter.drawRect(rect.normalized())




if __name__ == '__main__':
    app = QApplication(sys.argv)
    stream_app = Area()

    stream_app.setWindowFlag(Qt.FramelessWindowHint)
    stream_app.setWindowFlag(Qt.WindowTransparentForInput)
    stream_app.setWindowFlag(Qt.WindowStaysOnTopHint)

    stream_app.setAttribute(Qt.WA_NoSystemBackground, True)
    stream_app.setAttribute(Qt.WA_TranslucentBackground, True)

    stream_app.show()
    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        sys.exit()
    except SystemExit:
        print('closing...')