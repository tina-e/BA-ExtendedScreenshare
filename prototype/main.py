import threading
import time

from streamer.streamer import Streamer
from viewer.viewer import Viewer

import Config
import subprocess
import signal

from viewer.stream_window import StreamWindow
from gi.repository import GObject
from PyQt5.QtWidgets import *
import sys


streamer = None
viewer = None


def close(a, b):
    print(a, b)
    if Config.IS_STREAMER:
        streamer.close_stream()
    else:
        viewer.end_stream()
    exit(0)


if Config.IS_STREAMER:
    #signal.signal(signal.SIGINT, close)
    streamer = Streamer()
else:
    #signal.signal(signal.SIGINT, close)
    GObject.threads_init()
    app = QApplication(sys.argv)
    viewer = Viewer(app)
    viewer.access_stream()
    app.exec_()
    close()
    sys.exit(0)

signal.signal(signal.SIGINT, close)
while True:
    time.sleep(0.1)
    #try:
    #    time.sleep(1)
    #except KeyboardInterrupt:
    #    close()
    #    break

