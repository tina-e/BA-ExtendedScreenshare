
import time
import gi

gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")
from gi.repository import Gst, GLib, GstApp

STREAM_PORT = 5000
STREAMER_ADDRESS = '192.168.178.23'
RECEIVER_ADDRESS = '192.168.178.136'
START_X = 100
START_Y = 100
END_X = 500
END_Y = 500

Gst.init(None)
# https://gist.github.com/esrever10/7d39fe2d4163c5b2d7006495c3c911bb
# gst-launch-1.0 -v ximagesrc startx=50 starty=10 endx=800 endy=800 ! video/x-raw,framerate=20/1 ! videoscale ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=192.168.178.169 port=5111
# pipeline = Gst.parse_launch("ximagesrc startx=100 starty=10 endx=800 endy=800 ! video/x-raw,framerate=30/1 ! videoconvert ! x264enc ! rtph264pay config-interval=10 pt=96 ! udpsink host=192.168.178.136 host=8500")
pipeline = Gst.parse_launch(
        f"ximagesrc startx={START_X} starty={START_Y} endx={END_X} endy={END_Y} "
        "! video/x-raw,framerate=20/1 "
        "! videoscale "
        "! videoconvert "
        "! x264enc tune=zerolatency bitrate=500 speed-preset=superfast "
        "! rtph264pay "
        f"! udpsink host={RECEIVER_ADDRESS} port={STREAM_PORT} ")

print(pipeline, "opened")
pipeline.set_state(Gst.State.PLAYING)

while True:
    time.sleep(10)