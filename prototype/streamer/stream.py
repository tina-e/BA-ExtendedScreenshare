import gi
gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")
from gi.repository import Gst, GstApp
from streamer.frame_maker import FrameMaker


class Stream:
    def __init__(self, configurator):
        self.config = configurator
        Gst.init(None)
        self.pipeline = None
        self.frame_maker = None
        self.pipeline_open = False
        self.frame_maker = FrameMaker(self.config.START_X, self.config.START_Y, self.config.WIDTH, self.config.HEIGHT,
                                      self.config.BORDER_WIDTH, self.config.RESOLUTION_X, self.config.RESOLUTION_Y, self.config.PROJECT_PATH_ABSOLUTE)

    def setup(self):
        # https://gist.github.com/esrever10/7d39fe2d4163c5b2d7006495c3c911bb
        # gst-launch-1.0 -v ximagesrc startx=50 starty=10 endx=800 endy=800 ! video/x-raw,framerate=20/1 ! videoscale ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=192.168.178.169 port=5111
        # pipeline = Gst.parse_launch("ximagesrc startx=100 starty=10 endx=800 endy=800 ! video/x-raw,framerate=30/1 ! videoconvert ! x264enc ! rtph264pay config-interval=10 pt=96 ! udpsink host=192.168.178.136 host=8500")
        self.pipeline = Gst.parse_launch(
            f"ximagesrc startx={self.config.START_X} starty={self.config.START_Y} endx={self.config.END_X} endy={self.config.END_Y} "
            "! video/x-raw,framerate=20/1 "
            "! videoscale "
            "! videoconvert "
            "! x264enc tune=zerolatency bitrate=500 speed-preset=superfast "
            "! rtph264pay "
            f"! udpsink host={self.config.RECEIVER_ADDRESS} port={self.config.STREAM_PORT} ")
        print(self.pipeline, "opened")
        self.pipeline_open = True

    def on_mouse_pos_message(self, mouse_x, mouse_y):
        self.frame_maker.set_mouse_pos(mouse_x, mouse_y)

    def start(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        self.frame_maker.toggle_visibility()

    def end(self):
        self.pipeline.set_state(Gst.State.NULL)
        self.pipeline_open = False
        self.frame_maker.toggle_visibility()

    def close(self):
        self.end()
        self.pipeline = None
        self.frame_maker.end()

    def is_pipeline_playing(self):
        return self.pipeline_open
