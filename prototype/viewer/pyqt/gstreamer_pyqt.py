import time

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QSize
import sys

class VideoFeedWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def start(self):
        self.player = QMediaPlayer()
        self.resize(QSize(700, 700))

        self.STREAM_PORT = 5000
        self.RECEIVER_ADDRESS = '192.168.178.136'

        self.uri = (f"gst-pipeline: udpsrc address={self.RECEIVER_ADDRESS} port={self.STREAM_PORT} "
                "caps = \"application/x-rtp, media=(string)video, "
                "clock-rate=(int)90000, encoding-name=(string)H264, "
                "payload=(int)96\" ! rtph264depay ! decodebin  ! videoconvert ! autovideosink name=\"qtvideosink\"")

        #self.uri = 'videotestsrc'


        self.video_widget = QVideoWidget()

        self.player.setVideoOutput(self.video_widget)



        #self.player.setVideoOutput(self)
        #self.player.setMedia(QMediaContent(QUrl(uri)))
        #self.player.play()
        #self.layout = QVBoxLayout()
        #self.layout.addWidget(self.video_widget)
        #self.setLayout(self.layout)

    def play(self):
        self.player.setMedia(QMediaContent(QUrl(self.uri)))
        self.player.play()



app = QApplication(sys.argv)
win = VideoFeedWidget()
#win.raise_()
win.show()
win.start()
win.play()
sys.exit(app.exec_())
# while True:
#     time.sleep(1)

# öffnet zusätzliches Fenster statt ins qt-Fenster zu streamen