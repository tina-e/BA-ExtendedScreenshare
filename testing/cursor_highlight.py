import sys
import time

from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QFrame
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter, QPen

import Config_alt


class Highlight(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(Config_alt.START_X + 750, Config_alt.START_Y + 300, 22, 22)
        #self.setStyleSheet('border: 2px solid blue')

        self.frame = QFrame(self)
        self.frame.setGeometry(1, 1, 20, 20)
        self.frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.frame.setStyleSheet('border: 2px solid blue')
        self.frame.show()

        #layout = QVBoxLayout()
        #self.setLayout(layout)

        #self.pix = QPixmap(self.frame.size())
        #self.pix.fill(Qt.yellow)


    def move_highlight(self, x, y):
        self.setGeometry(x+self.x(), y+self.y(), 20, 20)

    #def paintEvent(self, event):
    #    painter = QPainter(self)
    #    painter.setOpacity(1)
    #    painter.drawPixmap(QPoint(), self.pix)


app = QApplication(sys.argv)
highlight = Highlight()
#highlight.setWindowFlag(Qt.FramelessWindowHint)
highlight.setWindowFlag(Qt.WindowTransparentForInput)
highlight.setWindowFlag(Qt.WindowStaysOnTopHint)
highlight.setAttribute(Qt.WA_NoSystemBackground, True)
highlight.setAttribute(Qt.WA_TranslucentBackground, True)
highlight.show()
'''time.sleep(1)
highlight.move_highlight(10, 10)
time.sleep(0.5)
highlight.move_highlight(15, 15)
time.sleep(0.5)
highlight.move_highlight(20, 20)
time.sleep(0.5)
highlight.move_highlight(25, 25)
time.sleep(0.5)
highlight.move_highlight(30, 30)
time.sleep(0.5)
highlight.move_highlight(35, 35)
time.sleep(0.5)
highlight.move_highlight(40, 40)'''
sys.exit(app.exec_())


