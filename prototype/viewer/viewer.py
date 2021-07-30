#gst-launch-1.0 -v udpsrc port=5000 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! autovideosink

import Config
from viewer.event_sender import EventSender
from viewer.stream_window import StreamWindow
from gi.repository import GObject
from PyQt5.QtWidgets import *
import sys
import subprocess

class Viewer:
    def __init__(self, app):
        print("Viewer alive")
        self.stream = None
        self.event_sender = EventSender()
        '''GObject.threads_init()
        app = QApplication(sys.argv)
        self.event_sender = EventSender()
        sys.exit(app.exec_())'''

    def access_stream(self):
        #print("Accessor benachrichten!")
        print("stream is goin to be opened")
        self.stream = StreamWindow()

        '''self.stream = subprocess.Popen(f"gst-launch-1.0 -v udpsrc address={Config.RECEIVER_ADDRESS} port={Config.STREAM_PORT} "
                         "caps = \"application/x-rtp, media=(string)video, "
                         "clock-rate=(int)90000, encoding-name=(string)H264, "
                         "payload=(int)96\" ! rtph264depay ! decodebin ! videoconvert ! autovideosink", shell=True)'''

        self.event_sender.on_view(True)
        #self.stream.get_stream_coords()


    def end_stream(self):
        #self.stream.terminate()
        self.stream.close()
        self.event_sender.on_view(False)