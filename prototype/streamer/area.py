import sys
import time

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QDialog
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter, QPen

import Config


class Area(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, Config.RESOLUTION_X, Config.RESOLUTION_Y)


        layout = QVBoxLayout()
        self.setLayout(layout)

        self.pix = QPixmap(self.rect().size())
        self.pix.fill(Qt.darkBlue)

        self.begin, self.destination = QPoint(), QPoint()
        self.rect = None
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0

    def get_coords(self):
        return self.start_x, self.start_y, self.end_x, self.end_y

    def paintEvent(self, event):
        print("paint")
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
            if self.begin.x() <= self.destination.x():
                self.start_x = self.begin.x()
                self.end_x = self.destination.x()
            else:
                self.start_x = self.destination.x()
                self.end_x = self.begin.x()

            if self.begin.y() <= self.destination.y():
                self.start_y = self.begin.y()
                self.end_y = self.destination.y()
            else:
                self.start_y = self.destination.y()
                self.end_y = self.begin.y()

            self.begin, self.destination = QPoint(), QPoint()
            self.update()
            self.hide()


    #todo: escape
    # def onKey: (self.done(0))

# https://www.youtube.com/watch?v=3QRBk-FpWjE