#gst-launch-1.0 -v udpsrc port=5000 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! autovideosink

import Config
from viewer.event_sender import EventSender
import subprocess

class Viewer:
    def __init__(self):
        print("Viewer alive")
        self.stream = None
        self.event_sender = EventSender()

    def access_stream(self):
        #print("Accessor benachrichten!")
        self.stream = subprocess.Popen(f"gst-launch-1.0 -v udpsrc address={Config.RECEIVER_ADDRESS} port={Config.STREAM_PORT} "
                         "caps = \"application/x-rtp, media=(string)video, "
                         "clock-rate=(int)90000, encoding-name=(string)H264, "
                         "payload=(int)96\" ! rtph264depay ! decodebin ! videoconvert ! autovideosink", shell=True)

        self.event_sender.on_view(True)


    def end_stream(self):
        self.stream.terminate()
        self.event_sender.on_view(False)