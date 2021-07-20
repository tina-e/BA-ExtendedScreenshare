import threading
import time

from streamer.streamer import Streamer
from viewer.viewer import Viewer

import Config
import subprocess
import signal


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
    viewer = Viewer()
    viewer.access_stream()

signal.signal(signal.SIGINT, close)
while True:
    pass
    #try:
    #    time.sleep(1)
    #except KeyboardInterrupt:
    #    close()
    #    break

