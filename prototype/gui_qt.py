import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QAction
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

import Config
from streamer.streamer import Streamer
from viewer.stream_window import StreamWindow
from streamer.area import Area

class Menu(QSystemTrayIcon):
    def __init__(self, icon, parent, stream_app):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.stream_app = stream_app
        self.streamer = None
        self.stream_viewer = None
        self.is_stream_paused = False

        menu = QMenu(parent)
        self.setContextMenu(menu)

        fullscreen_action = menu.addAction("Stream full screen")
        area_action = menu.addAction("Stream area")
        menu.addSeparator()
        play_action = menu.addAction("Play")
        pause_action = menu.addAction("Pause")
        menu.addSeparator()
        access_action = menu.addAction("Access Stream")
        menu.addSeparator()
        quit_action = menu.addAction("Quit")
        
        fullscreen_action.triggered.connect(self.setup_stream)
        area_action.triggered.connect(self.area)
        play_action.triggered.connect(self.play)
        pause_action.triggered.connect(self.pause)
        access_action.triggered.connect(self.access)
        quit_action.triggered.connect(self.quit)

    def setup_stream(self):
        print("setup stream")
        Config.IS_STREAMER = True
        Config.set_ips()
        if self.stream_viewer == None:
            self.streamer = Streamer()

    def area(self):
        print("area")
        self.stream_app.exec()
        dimensions = self.stream_app.get_coords()
        Config.set_coords(dimensions)
        self.setup_stream()

    def play(self):
        print("play")
        self.is_stream_paused = False

    def pause(self):
        print("pause")
        self.is_stream_paused = True

    def access(self):
        print("access")
        Config.IS_STREAMER = False
        Config.set_ips()
        if self.stream_viewer == None:
            self.stream_viewer = StreamWindow()

    def quit(self):
        print("end")
        QtCore.QCoreApplication.exit()


def main():
   app = QApplication(sys.argv)

   stream_app = Area()
   stream_app.setAttribute(Qt.WA_NoSystemBackground, True)
   stream_app.setAttribute(Qt.WA_TranslucentBackground, True)

   w = QWidget()
   trayIcon = Menu(QIcon("icon.png"), w, stream_app)
   trayIcon.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
    main()
