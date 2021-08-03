import sys
import socket
from event_types import EventTypes
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QAction
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

import Config
from streamer.streamer import Streamer
from viewer.stream_window import StreamWindow
from streamer.area import Area

class Menu(QSystemTrayIcon):
    def __init__(self, icon, parent):
        QSystemTrayIcon.__init__(self, icon, parent)
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
        area_choser = Area()
        area_choser.setWindowFlag(Qt.FramelessWindowHint)
        area_choser.setAttribute(Qt.WA_NoSystemBackground, True)
        area_choser.setAttribute(Qt.WA_TranslucentBackground, True)
        area_choser.exec()
        dimensions = area_choser.get_coords()
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
        self.register_to_stream()
        if self.stream_viewer == None:
            self.stream_viewer = StreamWindow()
            self.stream_viewer.show()

    def register_to_stream(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = EventTypes.REGISTER.to_bytes(1, 'big')
        print("REGISTER", message)
        sock.sendto(message, (Config.STREAMER_ADDRESS, Config.EVENT_PORT))
        sock.close()

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((Config.RECEIVER_ADDRESS, Config.EVENT_PORT))
        waiting_for_stream = True
        while waiting_for_stream:
            data, addr = sock.recvfrom(1024)
            print(data, addr)
            try:
                event_type = EventTypes(data[0])
                if event_type == EventTypes.STREAM_COORDS:
                    x = int.from_bytes(data[1:3], 'big')
                    y = int.from_bytes(data[3:5], 'big')
                    end_x = int.from_bytes(data[5:7], 'big')
                    end_y = int.from_bytes(data[7:9], 'big')
                    print(f"stream coords: {x} {y} {end_x} {end_y}")
                    Config.set_coords((x, y, end_x, end_y))
                    waiting_for_stream = False
            except UnicodeDecodeError:
                continue
        sock.close()


    def quit(self):
        print("end")
        if Config.IS_STREAMER and self.streamer is not None:
            self.streamer.close_stream()
        elif (not Config.IS_STREAMER) and (self.stream_viewer is not None):
            self.stream_viewer.close()
        QtCore.QCoreApplication.exit()


def main():
   app = QApplication(sys.argv)
   w = QWidget()
   trayIcon = Menu(QIcon("icon.png"), w)
   trayIcon.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
    main()
