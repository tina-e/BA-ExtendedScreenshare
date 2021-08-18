
import time

from PyQt5 import Qt
from PyQt5.QtGui import *
from PyQt5.QtCore import *
#from PyQt5.QtGui import QWidget, QLabel
from PyQt5.QtWidgets import *

import sys


class StreamWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setGeometry(2500, 500, 500, 500)
        self.setWindowFlag(Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.Transpa)
        self.setFocusPolicy(Qt.NoFocus)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowTitle('Streaming')
        self.gstWindowId = None
        self.x_pos = None
        self.y_pos = None
        self.setAcceptDrops(True)

    def simualte_drop(self):
        time.sleep(3)
        data = QMimeData()
        data.setText("test string to drop")
        drop_event = QDropEvent(QPointF(10, 10), Qt.CopyAction, data, Qt.LeftButton, Qt.NoModifier)
        self.dropEvent(drop_event)

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        event_content = event.mimeData().text()
        event_pos_x = event.pos().x()
        event_pos_y = event.pos().y()
        is_file = event.mimeData().hasFormat('COMPOUND_TEXT')

        print(event_pos_x)
        print(event_pos_y)
        print(event_content)

    def moveEvent(self, event):
        self.x_pos = self.pos().x()
        self.y_pos = self.pos().y()


app = QApplication(sys.argv)
win = StreamWindow()

win.show()

win.simualte_drop()

sys.exit(app.exec_())

