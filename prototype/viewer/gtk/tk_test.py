import sys
import os
import time

from functools import partial
import tkinter as tk

import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst

# Needed for set_window_handle():
gi.require_version('GstVideo', '1.0')
from gi.repository import GstVideo

import Config

APP_TITLE = "GStreamer"
APP_XPOS = 100
APP_YPOS = 100
APP_WIDTH = 400
APP_HEIGHT = 400


class Application(object):

    def __init__(self, master):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.close)

        self.main_frame = tk.Frame(master, relief='sunken', bd=6)
        self.main_frame.pack(padx=10, pady=10)

        self.display_frame = tk.Frame(self.main_frame, width=530, height=300,
                                      relief='sunken', bd=2)
        self.display_frame.pack()

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(expand=True, pady=(0, 10))

        tk.Button(self.button_frame, text="Start",
                  command=partial(self.video_control, 'start')).pack(side='left')
        tk.Button(self.button_frame, text="Pause",
                  command=partial(self.video_control, 'pause')).pack(side='left')
        tk.Button(self.button_frame, text="Stop",
                  command=partial(self.video_control, 'stop')).pack(side='left')

        self.var_time = tk.StringVar(master, "0:00")
        tk.Label(self.button_frame, textvariable=self.var_time, width=6,
                 bg='white').pack(side='left')
        self.frame_id = self.display_frame.winfo_id()

        self.player = Gst.ElementFactory.make('udpsrc', None)
        self.player.set_property('address', Config.RECEIVER_ADDRESS)
        self.player.set_property('port', Config.STREAM_PORT)

        #self.player = Gst.ElementFactory.make('udpsrc', None)
        #self.player.set_property('uri', f"udpsrc address={Config.RECEIVER_ADDRESS} port={Config.STREAM_PORT} "
        #                 "caps = \"application/x-rtp, media=(string)video, "
        #                 "clock-rate=(int)90000, encoding-name=(string)H264, "
        #                 "payload=(int)96\" ! rtph264depay ! decodebin ! videoconvert ! autovideosink")
        self.player.set_state(Gst.State.PLAYING)

        time.sleep(10)
        #bus = self.player.get_bus()
        #bus.enable_sync_message_emission()
        #bus.connect('sync-message::element', self.set_frame_handle,
        #            self.frame_id)

    def close(self):
        self.master.withdraw()
        self.player.set_state(Gst.State.NULL)
        self.master.destroy()

    def video_control(self, action):
        if action == 'start':
            duration_nanosecs = self.player.query_duration(Gst.Format.TIME)[1]
            duration = float(duration_nanosecs) / Gst.SECOND
            print("Dauer:", duration)

        elif action == 'pause':
            self.player.set_state(Gst.State.PAUSED)
            nanosecs = self.player.query_position(Gst.Format.TIME)[1]
            position = float(nanosecs) / Gst.SECOND
            print("Position:", position)

        elif action == 'stop':
            self.player.set_state(Gst.State.NULL)

    def set_frame_handle(self, bus, message, frame_id):
        if not message.get_structure() is None:
            if message.get_structure().get_name() == 'prepare-window-handle':
                display_frame = message.src
                display_frame.set_property('force-aspect-ratio', True)
                display_frame.set_window_handle(frame_id)


def main():
    app_win = tk.Tk()
    app_win.title(APP_TITLE)
    app_win.geometry("+{}+{}".format(APP_XPOS, APP_YPOS))
    # app_win.geometry("{}x{}".format(APP_WIDTH, APP_HEIGHT))

    Gst.init(None)

    app = Application(app_win)

    app_win.mainloop()


if __name__ == '__main__':
    main()