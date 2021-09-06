import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from config import Configurator
from streamer.area import Area
from streamer.streamer import Streamer
from viewer.stream_window import StreamWindow


class Menu(QSystemTrayIcon):
    def __init__(self, icon, parent, configurator):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.parent = parent
        self.config = configurator
        self.streamer = None
        self.stream_viewer = None
        self.is_stream_active = False

        menu = QMenu(self.parent)
        self.setContextMenu(menu)

        self.fullscreen_action = menu.addAction("Stream Full Screen")
        self.area_action = menu.addAction("Stream Area")
        menu.addSeparator()
        self.access_action = menu.addAction("Access Stream")
        menu.addSeparator()
        self.quit_action = menu.addAction("Quit")
        
        self.fullscreen_action.triggered.connect(self.setup_stream)
        self.area_action.triggered.connect(self.area)
        self.access_action.triggered.connect(self.access)
        self.quit_action.triggered.connect(self.quit)

    def setup_stream(self):
        print("setup stream")
        if self.streamer is None:
            self.area_action.setEnabled(False)
            self.fullscreen_action.setEnabled(False)
            self.access_action.setEnabled(False)
            self.config.IS_STREAMER = True
            self.config.set_streamer_ip(None)
            self.streamer = Streamer(self.config)

    def area(self):
        print("area")
        if self.streamer is None:
            self.open_area_chooser()

    def open_area_chooser(self):
        area_chooser = Area(self.config.RESOLUTION_X, self.config.RESOLUTION_Y)
        area_chooser.setWindowFlag(Qt.FramelessWindowHint)
        area_chooser.setAttribute(Qt.WA_NoSystemBackground, True)
        area_chooser.setAttribute(Qt.WA_TranslucentBackground, True)
        result = area_chooser.exec()
        if result == 1:
            dimensions = area_chooser.get_coords()
            self.config.set_coords(dimensions)
            self.setup_stream()
        elif result == 0:
            self.end()

    def access(self):
        if self.stream_viewer:
            self.stream_viewer.close()
            self.stream_viewer = None
        given_streamer_ip = self.get_ip_from_dialog()
        #given_streamer_ip = '192.168.178.23'
        if given_streamer_ip:
            self.init_receiving(given_streamer_ip)

    def init_receiving(self, given_streamer_ip):
        self.area_action.setEnabled(False)
        self.fullscreen_action.setEnabled(False)
        self.config.IS_STREAMER = False
        self.config.set_streamer_ip(given_streamer_ip)
        self.config.set_receiver_ip(None)
        self.config.write_clipboard_config()
        self.stream_viewer = StreamWindow(self.config)
        if self.stream_viewer.get_registration_state():
            self.stream_viewer.show()


    def get_ip_from_dialog(self):
        given_ip, accepted = QInputDialog.getText(self.parent, "IP Dialog", "Streamer IP:", QLineEdit.Normal, "")
        if accepted and given_ip != '':
            return given_ip
        return None

    def quit(self):
        print("quit")
        if self.config.IS_STREAMER and self.streamer is not None:
            self.streamer.close_stream()
        elif (not self.config.IS_STREAMER) and (self.stream_viewer is not None) and (self.stream_viewer.isVisible()):
            self.stream_viewer.close()
        self.config.clean_clipboard_config()
        QtCore.QCoreApplication.exit()
        exit(0)


def main():
    print(sys.argv)
    config = Configurator(sys.argv)
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    w = QWidget()
    tray_icon = Menu(QIcon("icon.png"), w, config)
    tray_icon.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
