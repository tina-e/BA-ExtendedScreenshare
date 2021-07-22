#self.stream = subprocess.Popen(f"gst-launch-1.0 -v udpsrc address={Config.RECEIVER_ADDRESS} port={Config.STREAM_PORT} "
#                         "caps = \"application/x-rtp, media=(string)video, "
#                         "clock-rate=(int)90000, encoding-name=(string)H264, "
#                         "payload=(int)96\" ! rtph264depay ! decodebin ! videoconvert ! autovideosink", shell=True)
import sys
import time

import gi
gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")
from gi.repository import Gst, GLib, GstApp, GstVideo, GObject
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl


Gst.init(None)

class StreamWindow(QMainWindow):
    def __init__(self, parent=None):
        super(StreamWindow, self).__init__(parent)

        self.display = QWidget()
        self.windowId = self.display.winId()

        self.setGeometry(60, 50, 640, 480)
        self.setWindowTitle("Streaming")

        self.STREAM_PORT = 5000
        self.RECEIVER_ADDRESS = '192.168.178.136'

        #self.player = QMediaPlayer()


    def setup_pipeline(self):
        # https://gist.github.com/esrever10/7d39fe2d4163c5b2d7006495c3c911bb
        # gst-launch-1.0 -v ximagesrc startx=50 starty=10 endx=800 endy=800 ! video/x-raw,framerate=20/1 ! videoscale ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=192.168.178.169 port=5111
        # pipeline = Gst.parse_launch("ximagesrc startx=100 starty=10 endx=800 endy=800 ! video/x-raw,framerate=30/1 ! videoconvert ! x264enc ! rtph264pay config-interval=10 pt=96 ! udpsink host=192.168.178.136 host=8500")
        self.pipeline = Gst.Pipeline()
        self.udp_source = Gst.ElementFactory.make('udpsrc', None)
        self.udp_source.set_property('address', self.RECEIVER_ADDRESS)
        self.udp_source.set_property('port', self.STREAM_PORT)
        self.pipeline.add(self.udp_source)

        stream_caps = Gst.Caps.from_string("application/x-rtp, media=(string)video, "
                                 "clock-rate=(int)90000, encoding-name=(string)H264, "
                                 "payload=(int)96")
        self.caps_filter = Gst.ElementFactory.make('capsfilter', None)
        self.caps_filter.set_property('caps', stream_caps)
        self.pipeline.add(self.caps_filter)
        self.udp_source.link(self.caps_filter)

        self.rtph264depay = Gst.ElementFactory.make('rtph264depay', None)
        self.pipeline.add(self.rtph264depay)
        self.udp_source.link(self.rtph264depay)

        self.decode = Gst.ElementFactory.make('decodebin', None)
        self.pipeline.add(self.decode)
        self.rtph264depay.link(self.decode)

        self.convert = Gst.ElementFactory.make('videoconvert', None)
        self.pipeline.add(self.convert)
        self.decode.link(self.convert)

        self.sink = Gst.ElementFactory.make("xvimagesink", "videosink")
        self.pipeline.add(self.sink)
        self.decode.link(self.sink)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect('sync-message::element', self.on_sync_message)

    def on_sync_message(self, bus, msg):
        if msg.get_structure().get_name() == 'prepare-window-handle':
            msg.src.set_window_handle(self.windowId)

    def start_pipeline(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        print("playing")


app = QApplication(sys.argv)
window = StreamWindow()
window.setup_pipeline()
window.start_pipeline()
window.show()
sys.exit(app.exec_())

# fehlermeldung: ** (python3.8:31230): CRITICAL **: 11:46:59.393: gst_capsfilter_prepare_buf: assertion 'out_caps != NULL' failed