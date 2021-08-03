#!/usr/bin/env python

# source: https://gist.github.com/JohnDMcMaster/fdedc262feebc44d0ce8399ad7652b38

'''
gst-launch-1.0 videotestsrc ! videoscale ! videoconvert ! ximagesink
'''


# https://wiki.ubuntu.com/Novacut/GStreamer1.0#Python_Porting_Guide
import time

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

import Config

gi.require_version('Gst', '1.0')
from gi.repository import Gst
Gst.init(None)
from gi.repository import GObject

from viewer.event_sender import EventSender

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
        self.setFixedWidth(Config.WIDTH)
        self.setFixedHeight(Config.HEIGHT)
        self.setWindowTitle('Streaming')
        self.gstWindowId = None
        self.x_pos = None
        self.y_pos = None
        self.event_sender = EventSender(self)
        self.setupGst()
        assert self.gstWindowId
        self.start_gstreamer()

    def moveEvent(self, event):
        self.x_pos = self.pos().x()
        self.y_pos = self.pos().y()

    def start_gstreamer(self):
        print("Starting gstreamer pipeline")
        self.player.set_state(Gst.State.PLAYING)
        self.event_sender.on_view(True)

    def setupGst(self):
        self.gstWindowId = self.winId()
        print("Setting up gstreamer pipeline, win id %s" % (self.gstWindowId,))

        self.player = Gst.parse_launch(f'udpsrc address={Config.RECEIVER_ADDRESS} port={Config.STREAM_PORT} caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! ximagesink name=sinkx_overview')
        #self.player = Gst.parse_launch('videotestsrc ! videoconvert ! videoscale ! ximagesink name=sinkx_overview')

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        #bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)

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


    def get_stream_coords(self):
        return self.x_pos, self.y_pos

    def update_stream_dimensions(self):
        self.setFixedWidth(Config.WIDTH)
        self.setFixedHeight(Config.HEIGHT)

    def is_active(self):
        return self.isActiveWindow()

    def get_position_in_stream(self, x, y):
        depth = self.style().pixelMetric(QStyle.PM_TitleBarHeight)
        x_calculated = x - self.x_pos
        y_calculated = y - self.y_pos - depth
        if 0 <= x_calculated <= self.width() and 0 <= y_calculated <= self.height():
            return x_calculated, y_calculated
        print("cursor out of stream")
        return None, None

    def closeEvent(self, event):
        print("end watching")
        self.event_sender.on_view(False)

