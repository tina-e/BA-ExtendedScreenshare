#!/usr/bin/env python

# Einbettung des GStreams orientiert an: https://gist.github.com/JohnDMcMaster/fdedc262feebc44d0ce8399ad7652b38

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import Gst
from gi.repository import GstVideo # eventually marked as unused but necessary
Gst.init(None)
from PyQt5.QtWidgets import *

from receiver.event_sender import EventSender
from receiver.file_communication_viewer import FileClient


class StreamWindow(QMainWindow):
    '''
    In this window, the stream is displayed.
    It's size corresponds to the size of the streamed region.
    The window allows drag-and-drop, so dropped files can be sent to the streamer.
    '''
    def __init__(self, configurator):
        QMainWindow.__init__(self)
        self.configurator = configurator
        self.event_sender = EventSender(self, self.configurator)
        self.registration_successful = self.event_sender.register()
        if self.registration_successful:
            self.setFixedWidth(configurator.WIDTH)
            self.setFixedHeight(configurator.HEIGHT)
            self.setWindowTitle('Streaming')
            self.gstWindowId = None
            self.x_pos = None
            self.y_pos = None

            self.setAcceptDrops(True)
            self.file_communicator = FileClient(configurator)
            self.file_communicator.connect()

            self.setupGst()
            assert self.gstWindowId
            self.start_gstreamer()

    def get_registration_state(self):
        return self.registration_successful

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        '''
        If a file was dropped into the stream,
        the file, the filename and the drop-position is sent to the server
        !! If there are spaces in the filename, QT represents them with '%20'.
        '''
        files = event.mimeData().text().rstrip('\n').split('\n')
        for listed_file in files:
            event_pos_x = event.pos().x()
            event_pos_y = event.pos().y()
            if event.mimeData().hasUrls():
                filename = listed_file.lstrip('file:')
                filename = filename.replace('%20', ' ')
                self.file_communicator.send_file(filename, event.mimeData().formats()[0], event_pos_x, event_pos_y)

    def moveEvent(self, event):
        self.x_pos = self.pos().x()
        self.y_pos = self.pos().y()

    def start_gstreamer(self):
        self.player.set_state(Gst.State.PLAYING)
        self.event_sender.on_view(True)

    def setupGst(self):
        '''
        The Gstreamer-pipeline is launches inside the QWidget.
        If there is movement within the stream, the view gets updated
        '''
        self.gstWindowId = self.winId()
        self.player = Gst.parse_launch(f'udpsrc port={self.configurator.STREAM_PORT} caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! ximagesink name=sinkx_overview')

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)

    def on_message(self, bus, message):
        t = message.type

    def on_sync_message(self, bus, message):
        structure = message.get_structure()
        if structure is None:
            return
        message_name = structure.get_name()
        if message_name == "prepare-window-handle":
            assert message.src.get_name() == 'sinkx_overview'
            assert self.gstWindowId
            message.src.set_window_handle(self.gstWindowId)

    def get_stream_coords(self):
        return self.x_pos, self.y_pos

    def is_active(self):
        return self.isActiveWindow()

    def get_position_in_stream(self, x, y):
        depth = self.style().pixelMetric(QStyle.PM_TitleBarHeight)
        x_calculated = x - self.x_pos
        y_calculated = y - self.y_pos - depth
        if 0 <= x_calculated <= self.width() and 0 <= y_calculated <= self.height():
            return x_calculated, y_calculated
        return None, None

    def closeEvent(self, event):
        '''
        when an active stream-window is closed,
        all related components are closed.
        Also the streamer is informed.
        '''
        if self.registration_successful:
            self.player.set_state(Gst.State.NULL)
            self.event_sender.on_view(False)
            self.file_communicator.close_connection()
