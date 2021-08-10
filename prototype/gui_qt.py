import sys
import socket
from event_types import EventTypes
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QAction
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

#import Config
from Config2 import Config
from streamer.streamer import Streamer
from viewer.stream_window import StreamWindow
from streamer.area import Area

class Menu(QSystemTrayIcon):
    def __init__(self, icon, parent):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.config = Config()
        self.streamer = None
        self.stream_viewer = None
        self.is_stream_active = False

        menu = QMenu(parent)
        self.setContextMenu(menu)

        self.fullscreen_action = menu.addAction("Stream Full Screen")
        self.area_action = menu.addAction("Stream Area")
        menu.addSeparator()
        self.access_action = menu.addAction("Access Stream")
        menu.addSeparator()
        self.end_action = menu.addAction("Stop Stream")
        menu.addSeparator()
        self.quit_action = menu.addAction("Quit")
        
        self.fullscreen_action.triggered.connect(self.setup_stream)
        self.area_action.triggered.connect(self.area)
        self.access_action.triggered.connect(self.access)
        self.end_action.triggered.connect(self.end)
        self.quit_action.triggered.connect(self.quit)

        self.end_action.setEnabled(False)

        #self.play_action = menu.addAction("Play")
        #self.pause_action = menu.addAction("Pause")
        # self.play_action.triggered.connect(self.play)
        # self.pause_action.triggered.connect(self.pause)
        #self.play_action.setEnabled(False)
        #self.pause_action.setEnabled(False)

    def setup_stream(self):
        print("setup stream")
        if self.streamer is None:
            self.end_action.setEnabled(True)
            self.area_action.setEnabled(False)
            self.fullscreen_action.setEnabled(False)
            self.config.IS_STREAMER = True
            self.config.set_ips()
            self.streamer = Streamer(self.config)

    def area(self):
        print("area")
        if self.streamer is None:
            self.open_area_chooser()
            self.setup_stream()
        #else:
        #    self.end()
        #    self.open_area_choser()
        #    self.streamer.start_stream()

    def open_area_chooser(self):
        area_chooser = Area(self.config.RESOLUTION_X, self.config.RESOLUTION_Y)
        area_chooser.setWindowFlag(Qt.FramelessWindowHint)
        area_chooser.setAttribute(Qt.WA_NoSystemBackground, True)
        area_chooser.setAttribute(Qt.WA_TranslucentBackground, True)
        area_chooser.exec()
        dimensions = area_chooser.get_coords()
        self.config.set_coords(dimensions)

    def access(self):
        if self.stream_viewer is None or not self.stream_viewer.isVisible():
            print("access")
            self.config.IS_STREAMER = False
            self.config.set_ips()
            print("s", self.config.STREAMER_ADDRESS)
            print("r", self.config.RECEIVER_ADDRESS)
            self.register_to_stream()
            self.stream_viewer = StreamWindow(self.config)
            self.stream_viewer.show()
            self.end_action.setEnabled(True)

    def register_to_stream(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = EventTypes.REGISTER.to_bytes(1, 'big')
        print("REGISTER", message)
        sock.sendto(message, (self.config.STREAMER_ADDRESS, self.config.EVENT_PORT))
        sock.close()

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.config.RECEIVER_ADDRESS, self.config.EVENT_PORT))
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
                    self.config.set_coords((x, y, end_x, end_y))
                    waiting_for_stream = False
            except UnicodeDecodeError:
                continue
        sock.close()

    def end(self):
        print("end") #todo: if streamer: causes SIGSEGV/SIGABRT
        self.end_action.setEnabled(False)
        self.fullscreen_action.setEnabled(True)
        self.area_action.setEnabled(True)
        if self.config.IS_STREAMER and self.streamer is not None:
            self.streamer.close_stream()
        elif (not self.config.IS_STREAMER) and (self.stream_viewer is not None) and (self.stream_viewer.isVisible()):
            self.stream_viewer.close()

    def quit(self):
        print("quit")
        if self.config.IS_STREAMER:
            if self.streamer is None or self.streamer.is_stream_open():
                self.end()
        else:
            if self.stream_viewer is None or self.stream_viewer.isVisible():
                self.end()
        QtCore.QCoreApplication.exit()


    '''def play(self):
        print("play")
        self.streamer.play_again_stream()
        self.pause_action.setEnabled(True)
        self.play_action.setEnabled(False)

    def pause(self):
        print("pause")
        self.streamer.pause_stream()
        self.play_action.setEnabled(True)
        self.pause_action.setEnabled(False)'''


def main():
   app = QApplication(sys.argv)
   app.setQuitOnLastWindowClosed(False)
   w = QWidget()
   trayIcon = Menu(QIcon("icon.png"), w)
   trayIcon.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
    main()
