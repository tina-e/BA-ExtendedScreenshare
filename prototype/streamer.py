from threading import Thread
import time

# https://www.youtube.com/watch?v=HDY8pf-b1nA
# sudo apt install python3-gst-1.0
import gi
gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")
from gi.repository import Gst, GLib, GstApp
from evdev import UInput, ecodes
import Config

class Streamer:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.pipeline = None
        Gst.init(None)
        main_loop = GLib.MainLoop()
        main_loop_thread = Thread(target=main_loop.run)
        main_loop_thread.start()
        self.add_cursor()

    def open_stream(self):
        # https://gist.github.com/esrever10/7d39fe2d4163c5b2d7006495c3c911bb
        # gst-launch-1.0 -v ximagesrc startx=50 starty=10 endx=800 endy=800 ! video/x-raw,framerate=20/1 ! videoscale ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=192.168.178.169 port=5111
        # pipeline = Gst.parse_launch("ximagesrc startx=100 starty=10 endx=800 endy=800 ! video/x-raw,framerate=30/1 ! videoconvert ! x264enc ! rtph264pay config-interval=10 pt=96 ! udpsink host=192.168.178.136 host=8500")
        self.pipeline = Gst.parse_launch(
            f"ximagesrc startx={self.start_x} starty={self.start_y} endx={self.end_x} endy={self.end_y} "
            "! video/x-raw,framerate=20/1 "
            "! videoscale "
            "! videoconvert "
            "! x264enc tune=zerolatency bitrate=500 speed-preset=superfast "
            "! rtph264pay "
            f"! udpsink host={Config.RECEIVER} port={Config.STREAM_PORT} ")
        print(self.pipeline, "opened")

    def start_stream(self):
        self.pipeline.set_state(Gst.State.PLAYING)

    def pause_stream(self):
        self.pipeline.set_state(Gst.State.PAUSED)

    def move_stream(self):
        self.pause_stream()
        self.start_x = 200
        self.start_y = 200
        self.open_stream()
        self.start_stream()

    #def end_stream(self):
        #TODO

    def add_cursor(self):
        # specify capabilities for our virtual input device
        cap_mouse = {
            ecodes.EV_REL: (ecodes.REL_X, ecodes.REL_Y),
            ecodes.EV_KEY: (ecodes.BTN_LEFT, ecodes.BTN_RIGHT),
        }
        with UInput(cap_mouse, name="mouse") as mouse_ui:
            mouse_ui.write(ecodes.EV_REL, ecodes.REL_X, self.start_x)
            mouse_ui.write(ecodes.EV_REL, ecodes.REL_Y, self.start_y)
            mouse_ui.syn()

##############################################################################################################################

# ! video/x-raw,width=750,height=500   legt größe des streams fest
# use-damage=0 angeblich CPU fordernd
# ximageslink creates window for output (glimagesink also possible, higher CPU required)
# ! videoscale method=0, auch wieder CPU sache scheinbar
# pipeline = Gst.parse_launch("ximagesrc startx=100 starty=10 endx=800 endy=800 ! video/x-raw,framerate=30/1 ! ximagesink")

# pipeline = Gst.parse_launch("rtpmp4vpay ! decodebin ! videoconvert ! autovideosink")
# pipeline = Gst.parse_launch("v4l2src ! decodebin ! videoconvert ! appsink name=sink")
# appsink = pipeline.get_by_name("sink")
# pipeline.set_state(Gst.State.PLAYING)