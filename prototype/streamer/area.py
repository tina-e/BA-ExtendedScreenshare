import sys
import time

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter, QPen

import Config


class Area(QWidget):
    def __init__(self):
        super().__init__()
        print("open")
        self.setGeometry(0, 0, Config.RESOLUTION_X*2, Config.RESOLUTION_Y)
        #self.window_width = 750
        #self.window_height = 500
        #self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.pix = QPixmap(self.rect().size())
        self.pix.fill(Qt.darkBlue)

        self.begin, self.destination = QPoint(), QPoint()
        self.rect = None


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(0.2)
        painter.drawPixmap(QPoint(), self.pix)
        if not self.begin.isNull() and not self.destination.isNull():
            pen = QPen(Qt.white, 2)
            painter.setPen(pen)
            self.rect = QRect(self.begin, self.destination)
            painter.drawRect(self.rect.normalized())


    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.begin = event.pos()
            self.destination = self.begin
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.destination = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() & Qt.LeftButton:
            self.begin, self.destination = QPoint(), QPoint()
            self.update()
            #todo: open stream/frame
            self.hide()


# https://www.youtube.com/watch?v=3QRBk-FpWjE