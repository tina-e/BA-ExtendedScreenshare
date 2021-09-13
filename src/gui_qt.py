import sys
import signal
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTimer

from config import Configurator
from streamer.area import Area
from streamer.streamer import Streamer
from receiver.stream_window import StreamWindow

app = None
tray_icon = None

class Menu(QSystemTrayIcon):
    '''
    This is the Main-Menu of the application.
    From here, you can start streaming or access a stream.
    You can also quit the application.
    '''
    def __init__(self, icon, parent, configurator):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.parent = parent
        self.config = configurator
        self.streamer = None
        self.stream_receiver = None
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

    def area(self):
        if self.streamer is None:
            self.open_area_chooser()

    def open_area_chooser(self):
        '''
        A semi-trasparent interface shows up. There you can choose the shared region.
        If the QDialog (AreaChooser) is accepted, the stream will be set up.
        '''
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

    def setup_stream(self):
        '''
        During an active stream, all other menu-options will be disabled (prototypically).
        Startes the stream.
        '''
        if self.streamer is None:
            self.area_action.setEnabled(False)
            self.fullscreen_action.setEnabled(False)
            self.access_action.setEnabled(False)
            self.config.IS_STREAMER = True
            self.config.set_streamer_ip(None)
            self.streamer = Streamer(self.config)

    def access(self):
        '''
        If already watching a stream: close the existing stream.
        Set up new stream-window for stream at given IP.
        '''
        if self.stream_receiver:
            if self.stream_receiver.isVisible():
                self.stream_receiver.close()
            del self.stream_receiver
        given_streamer_ip = self.get_ip_from_dialog()
        # given_streamer_ip = '192.168.178.23'
        if given_streamer_ip:
            self.setup_receiver(given_streamer_ip)

    def setup_receiver(self, given_streamer_ip):
        '''
        During watching a stream, the option to stream will be disables (prototypically)
        The stream-window is set up and shown if a stream could be accessed.
        '''
        self.area_action.setEnabled(False)
        self.fullscreen_action.setEnabled(False)
        self.config.IS_STREAMER = False
        self.config.set_streamer_ip(given_streamer_ip)
        self.config.set_receiver_ip(None)
        self.stream_receiver = StreamWindow(self.config)
        if self.stream_receiver.get_registration_state():
            self.stream_receiver.show()

    def get_ip_from_dialog(self):
        '''
        A QDialog for typing the streamer's IP is shown.
        '''
        given_ip, accepted = QInputDialog.getText(self.parent, "Connecting...", "Streamer's IP-Address:", QLineEdit.Normal, "")
        if accepted and given_ip != '':
            return given_ip
        return None

    def quit(self):
        '''
        If there is an active stream, it will be closed before the exit of the application.
        '''
        if self.config.IS_STREAMER and self.streamer is not None:
            self.streamer.close_stream()
        elif (not self.config.IS_STREAMER) and (self.stream_receiver is not None) and (self.stream_receiver.isVisible()):
            self.stream_receiver.close()
        QtCore.QCoreApplication.exit()
        exit(0)


def handle_sigint(*args):
    '''
    Allows the user to quit the application with KeyboardInterrupt.
    '''
    global app, tray_icon
    tray_icon.quit()
    app.quit()


def main():
    global app, tray_icon
    signal.signal(signal.SIGINT, handle_sigint)
    config = Configurator(sys.argv)
    app = QApplication(sys.argv)

    # for quitting with KeyboardInterrupt
    timer = QTimer()
    timer.start(100)
    timer.timeout.connect(lambda: None)

    app.setAttribute(Qt.AA_X11InitThreads)
    app.setQuitOnLastWindowClosed(False)
    w = QWidget()
    tray_icon = Menu(QIcon("img/icon.png"), w, config)
    tray_icon.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
