#gst-launch-1.0 -v udpsrc port=5000 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! autovideosink
import subprocess
import time

import Config
import window_manager
from ewmh import EWMH
ewmh = EWMH()

class Accessor:
    def __init__(self):
        print("Accessor alive")

    def access_stream(self):
        print("Accessor benachrichten!") #TODO
        subprocess.Popen(f"gst-launch-1.0 -v udpsrc address={Config.RECEIVER_ADDRESS} port={Config.STREAM_PORT} "
                         "caps = \"application/x-rtp, media=(string)video, "
                         "clock-rate=(int)90000, encoding-name=(string)H264, "
                         "payload=(int)96\" ! rtph264depay ! decodebin ! videoconvert ! autovideosink", shell=True)
        while True:
            if window_manager.is_stream_open():
                return
            time.sleep(0.5)
