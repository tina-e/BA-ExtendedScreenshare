#self.stream = subprocess.Popen(f"gst-launch-1.0 -v udpsrc address={Config.RECEIVER_ADDRESS} port={Config.STREAM_PORT} "
#                         "caps = \"application/x-rtp, media=(string)video, "
#                         "clock-rate=(int)90000, encoding-name=(string)H264, "
#                         "payload=(int)96\" ! rtph264depay ! decodebin ! videoconvert ! autovideosink", shell=True)
import time

import gi
gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")
from gi.repository import Gst, GLib, GstApp
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

#app = QtWidgets.
class StreamWindow(QMainWindow):
    def __init__(self, parent=None):
        super(StreamWindow, self).__init__(parent)

        STREAM_PORT = 5000
        RECEIVER_ADDRESS = '192.168.178.136'

        Gst.init(None)
                # https://gist.github.com/esrever10/7d39fe2d4163c5b2d7006495c3c911bb
                # gst-launch-1.0 -v ximagesrc startx=50 starty=10 endx=800 endy=800 ! video/x-raw,framerate=20/1 ! videoscale ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=192.168.178.169 port=5111
                # pipeline = Gst.parse_launch("ximagesrc startx=100 starty=10 endx=800 endy=800 ! video/x-raw,framerate=30/1 ! videoconvert ! x264enc ! rtph264pay config-interval=10 pt=96 ! udpsink host=192.168.178.136 host=8500")
        pipeline = Gst.parse_launch(f"udpsrc address={RECEIVER_ADDRESS} port={STREAM_PORT} "
                                 "caps = \"application/x-rtp, media=(string)video, "
                                 "clock-rate=(int)90000, encoding-name=(string)H264, "
                                 "payload=(int)96\" ! rtph264depay ! decodebin ! videoconvert ! autovideosink")

        pipeline.set_state(Gst.State.PLAYING)

win = StreamWindow()