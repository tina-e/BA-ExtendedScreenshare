#gst-launch-1.0 -v udpsrc port=5000 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! autovideosink
import subprocess
import time

from gi.repository import Gst, GLib, GstApp
import prototype.Config as Config
import prototype.window_manager as window_manager
from event_sender import EventSender
#from ewmh import EWMH
#ewmh = EWMH()

class Viewer:
    def __init__(self):
        print("Viewer alive")
        self.stream = None
        self.event_sender = EventSender()

    def access_stream(self):
        print("Accessor benachrichten!")
        self.stream = subprocess.Popen(f"gst-launch-1.0 -v udpsrc address={Config.RECEIVER_ADDRESS} port={Config.STREAM_PORT} "
                         "caps = \"application/x-rtp, media=(string)video, "
                         "clock-rate=(int)90000, encoding-name=(string)H264, "
                         "payload=(int)96\" ! rtph264depay ! decodebin ! videoconvert ! autovideosink", shell=True)
        self.event_sender.on_view(True)

        #while True:
        #    if window_manager.is_stream_open():
        #        return
        #    time.sleep(0.5)

    def end_stream(self):
        self.stream.terminate()
        self.event_sender.on_view(False)