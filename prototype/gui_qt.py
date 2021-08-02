import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QAction
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

import Config
from streamer.streamer import Streamer
from viewer.stream_window import StreamWindow

class Menu(QSystemTrayIcon):
    def __init__(self, icon, parent):
        QSystemTrayIcon.__init__(self, icon, parent)

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
        streamer = Streamer()

    def area(self):
        print("area")
        self.stream_app.exec()
        dimensions = self.stream_app.get_coords()
        Config.set_coords(dimensions)
        self.setup_stream()

    def play(self):
        print("play")

    def pause(self):
        print("pause")

    def access(self):
        print("access")
        Config.IS_STREAMER = False
        Config.set_ips()
        stream_viewer = StreamWindow()

    def quit(self):
        print("end")
        QtCore.QCoreApplication.exit()


def main():
   app = QApplication(sys.argv)
   w = QWidget()
   trayIcon = Menu(QIcon("icon.png"), w)
   trayIcon.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
    main()
