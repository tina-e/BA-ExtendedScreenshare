from prototype.streamer.frame_maker import FrameMaker
import Config
import gi
gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")
from gi.repository import Gst, GLib, GstApp


class Stream:
    def __init__(self):
        Gst.init(None)
        # https://gist.github.com/esrever10/7d39fe2d4163c5b2d7006495c3c911bb
        # gst-launch-1.0 -v ximagesrc startx=50 starty=10 endx=800 endy=800 ! video/x-raw,framerate=20/1 ! videoscale ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=192.168.178.169 port=5111
        # pipeline = Gst.parse_launch("ximagesrc startx=100 starty=10 endx=800 endy=800 ! video/x-raw,framerate=30/1 ! videoconvert ! x264enc ! rtph264pay config-interval=10 pt=96 ! udpsink host=192.168.178.136 host=8500")
        self.pipeline = Gst.parse_launch(
            f"ximagesrc startx={Config.START_X} starty={Config.START_Y} endx={Config.END_X} endy={Config.END_Y} "
            "! video/x-raw,framerate=20/1 "
            "! videoscale "
            "! videoconvert "
            "! x264enc tune=zerolatency bitrate=500 speed-preset=superfast "
            "! rtph264pay "
            f"! udpsink host={Config.RECEIVER_ADDRESS} port={Config.STREAM_PORT} ")
        print(self.pipeline, "opened")
        self.frame_maker = FrameMaker()

    def start(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        self.frame_maker.toggle_visibility()

    def end(self):
        self.pipeline.set_state(Gst.State.NULL)
        self.frame_maker.toggle_visibility()

    def close(self):
        self.end()
        self.pipeline = None
        self.frame_maker.end()
