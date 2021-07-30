#!/usr/bin/env python

# source: https://gist.github.com/JohnDMcMaster/fdedc262feebc44d0ce8399ad7652b38

'''
gst-launch-1.0 videotestsrc ! videoscale ! videoconvert ! ximagesink
'''


# https://wiki.ubuntu.com/Novacut/GStreamer1.0#Python_Porting_Guide

from PyQt5 import Qt
from PyQt5.QtGui import *
from PyQt5.QtCore import *
#from PyQt5.QtGui import QWidget, QLabel
from PyQt5.QtWidgets import *

import sys
import traceback
import os
import signal

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
Gst.init(None)
from gi.repository import GObject

from PIL import Image

if 1:
    gi.require_version('GstVideo', '1.0')
    # ??? why is this needed? does it do some magic under the hood?
    # "Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:"
    #from gi.repository import GdkX11, GstVideo
    from gi.repository import GstVideo

class StreamWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        #self.showMaximized()

        self.initUI()

        self.gstWindowId = None
        self.source = Gst.ElementFactory.make("videotestsrc", "video-source")
        self.setupGst()
        assert self.gstWindowId

        def init_x1_unreliable():
            self.start_gstreamer()
            self.show()

        def init_x1_reliable1():
            self.timer = QTimer()
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(self.start_gstreamer)
            self.timer.start(100)

            self.show()

        def init_x1_reliable2():
            self.show()
            self.start_gstreamer()

        #init_x1_unreliable()
        #init_x1_reliable1()
        init_x1_reliable2()

    def start_gstreamer(self):
        print("Starting gstreamer pipeline")
        self.player.set_state(Gst.State.PLAYING)

    def get_video_layout(self):
        # Overview
        def low_res_layout():
            layout = QVBoxLayout()
            layout.addWidget(QLabel("Overview"))

            # Raw X-windows canvas
            self.video_container = QWidget()
            w, h = 3264/4, 2448/4
            self.video_container.setMinimumSize(w, h)
            self.video_container.resize(w, h)
            policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.video_container.setSizePolicy(policy)

            layout.addWidget(self.video_container)

            return layout

        layout = QHBoxLayout()
        layout.addLayout(low_res_layout())
        return layout

    def setupGst(self):
        self.gstWindowId = self.video_container.winId()
        print("Setting up gstreamer pipeline, win id %s" % (self.gstWindowId,))

        #self.player = Gst.Pipeline()
        #sinkx = Gst.ElementFactory.make("ximagesink", 'sinkx_overview')
        ##sinkx = Gst.ElementFactory.make("xvimagesink", 'sinkx_overview')
        #self.videoconvert =  Gst.ElementFactory.make("videoconvert")
        #self.videoscale =  Gst.ElementFactory.make("videoscale")

        ## Video render stream
        #self.player.add(self.source)
        #self.player.add(self.videoconvert)
        #self.player.add(self.videoscale)
        #self.player.add(sinkx)
        #self.source.link(self.videoscale)
        #self.videoscale.link(self.videoconvert)
        #self.videoconvert.link(sinkx)

        self.player = Gst.parse_launch('udpsrc port=5000 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! ximagesink name=sinkx_overview')
        #self.player = Gst.parse_launch('videotestsrc ! videoconvert ! videoscale ! ximagesink name=sinkx_overview')

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)

    def on_message(self, bus, message):
        t = message.type

        #print('\n'.join(dir(gst)))
        print('MSG: %s' % (t,))
        return
        if t == Gst.Message.EOS:
            self.player.set_state(Gst.State.NULL)
            print("  End of stream")
        elif t == Gst.Message.STREAM_STATUS:
            print('  status')
        elif t == Gst.Message.STATE_CHANGED:
            state = self.player.get_state()
            s1, s2, s3 = state
            print('  %s, %s' % (Gst.element_state_get_name(s2), Gst.element_state_get_name(s3)))
        elif t == Gst.Message.ERROR:
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)
            self.player.set_state(Gst.State.NULL)

    def on_sync_message(self, bus, message):
        print('sync, %s' % (message,))
        structure = message.get_structure()
        if structure is None:
            return
        message_name = structure.get_name()
        if message_name == "prepare-window-handle":
            assert message.src.get_name() == 'sinkx_overview'

            # "Note that trying to get the drawingarea XID in your on_sync_message() handler will cause a segfault because of threading issues."
            #print 'sinkx_overview win_id: %s (%s)' % (self.gstWindowId, self.video_container.winId())
            assert self.gstWindowId
            #print(dir(message.src))
            message.src.set_window_handle(self.gstWindowId)

    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Streaming')

        # top layout
        layout = QHBoxLayout()

        layout.addLayout(self.get_video_layout())

        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

    def get_stream_coords(self):
        x = 0
        y = 0
        width = 100
        height = 100
        return x, y, width, height

    def is_active(self):
        return self.isActiveWindow()

def excepthook(excType, excValue, tracebackobj):
    print('%s: %s' % (excType, excValue))
    traceback.print_tb(tracebackobj)
    os._exit(1)

if __name__ == '__main__':
    if 1:
        sys.excepthook = excepthook
        # Exit on ^C instead of ignoring
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    GObject.threads_init()

    app = QApplication(sys.argv)
    #qApp.connect(qApp, SIGNAL('lastWindowClosed()'), qApp, SLOT('quit()'))
    _gui = StreamWindow()
    sys.exit(app.exec_())
