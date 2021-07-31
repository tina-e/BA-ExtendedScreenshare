import time

from streamer.streamer import Streamer

#from viewer.viewer import Viewer
from viewer.stream_window import StreamWindow

import Config
import signal

from gi.repository import GObject
from PyQt5.QtWidgets import *
import sys


streamer = None
viewer = None


def close():
    print()
    if Config.IS_STREAMER:
        streamer.close_stream()
    exit(0)


if Config.IS_STREAMER:
    #signal.signal(signal.SIGINT, close)
    streamer = Streamer()
else:
    #signal.signal(signal.SIGINT, close)
    GObject.threads_init()
    app = QApplication(sys.argv)
    stream_window = StreamWindow()
    sys.exit(app.exec_())

signal.signal(signal.SIGINT, close)
while True:
    time.sleep(0.1)
    #try:
    #    time.sleep(1)
    #except KeyboardInterrupt:
    #    close()
    #    break

