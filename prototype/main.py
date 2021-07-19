import threading
import time

from streamer.streamer import Streamer
from viewer.viewer import Viewer

import Config
import subprocess


streamer = None
viewer = None


def close():
    if Config.IS_STREAMER:
        streamer.end_stream()
    else:
        viewer.end_stream()


if Config.IS_STREAMER:
    #signal.signal(signal.SIGINT, close)
    streamer = Streamer()
else:
    #signal.signal(signal.SIGINT, close)
    viewer = Viewer()
    viewer.access_stream()


while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        close()
        break

