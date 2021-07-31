import threading

from PIL import Image, ImageDraw
from pystray import Icon, Menu as menu, MenuItem as item
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from io import BytesIO
import os
import subprocess
import platform
import base64
import sys

import Config
from prototype.streamer.area import Area
from prototype.streamer.streamer import Streamer
from prototype.viewer.viewer import Viewer


class Tray():
    def __init__(self, app_name, stream_app):
        self.app = app
        self.stream_app = stream_app
        self.app_name = app_name
        self.icon = Icon(
            self.app_name,
            icon=self.get_icon(),
            menu=menu(
                item(
                    'Stream full screen',
                    lambda item: self.setup_stream(),
                ),
                item(
                    'Stream region',
                    lambda item: self.open_area(),
                ),
                menu.SEPARATOR,
                item(
                    'Play',  # 1
                    lambda item: self.play_stream(0),
                ),
                item(
                    'Pause',  # 0
                    lambda item: self.play_stream(1),
                ),
                menu.SEPARATOR,
                item(
                    'Access stream',
                    lambda item: self.access_stream(),
                ),
                menu.SEPARATOR,
                item(
                    'Quit',
                    lambda icon: self.onclick_quit()
                )
            )
        )


    def setup_stream(self):
        Config.IS_STREAMER = True
        Config.set_ips()
        streamer = Streamer()

    def open_area(self):
        self.stream_app.exec()
        dimensions = self.stream_app.get_coords()
        Config.set_coords(dimensions)
        self.setup_stream()

    def play_stream(self, playing):
        return

    def access_stream(self):
        Config.IS_STREAMER = False
        Config.set_ips()
        viewer = Viewer()
        viewer.access_stream()


    def get_icon(self):
        return Image.open(BytesIO(base64.b64decode(self.get_app_icon())))

    def run(self):
        self.icon.run(self.setup)

    def onclick_quit(self):
        self.icon.stop()

    def setup(self, icon):
        self.icon.visible = True

    def get_app_icon(self):
        return """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"""


app = QApplication(sys.argv)
stream_app = Area()
stream_app.setAttribute(Qt.WA_NoSystemBackground, True)
stream_app.setAttribute(Qt.WA_TranslucentBackground, True)

tray = Tray("Advanced Screen Share", stream_app)
tray.run()

sys.exit(app.exec_())
