import sys
import os
import subprocess
import re
import time

from ewmh import EWMH

#TODO
class WindowManager:
    def __init__(self):
        self.ewmh = EWMH()
        self.x = self.y = self.width = self.height = self.depth = 0

    def __set_stream_coords(self):
        time.sleep(10)
        self.x, self.y, self.width, self.height, self.depth = self.__get_stream_coordinates()

    def __get_stream_coordinates(self):
        win_geo = None
        open_wins = self.ewmh.getClientList()
        for win in open_wins:
            if win.get_wm_class() == ('gst-launch-1.0', 'GStreamer'):
            #if win.get_wm_class() == ('jetbrains-pycharm-ce', 'jetbrains-pycharm-ce'):
                win_geo = self.__frame(win).get_geometry()
                break
        return win_geo.x, win_geo.y, win_geo.width, win_geo.height, win_geo.depth

    def __frame(self, window):
        framed_window = window
        while framed_window.query_tree().parent != self.ewmh.root:
            framed_window = framed_window.query_tree().parent
        return framed_window

    def is_in_focus_old(self):
        window = self.ewmh.getActiveWindow()
        # return window.get_wm_class() == ('gst-launch-1.0', 'GStreamer')
        return window.get_wm_class() == ('jetbrains-pycharm-ce', 'jetbrains-pycharm-ce')

    def get_pos_in_stream(self, x, y):
        rel_x = x - self.x
        rel_y = y - self.y
        if 0 <= rel_x <= self.width and 0 <= rel_y <= self.height:
            return rel_x, rel_y
        print("cursor out of stream")
        return None, None


    # https://stackoverflow.com/questions/10266281/obtain-active-window-using-python
    def is_in_focus(self):
        root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
        stdout, stderr = root.communicate()

        m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
        if m != None:
            window_id = m.group(1)
            window = subprocess.Popen(['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE)
            stdout, stderr = window.communicate()
        else:
            return False

        match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", stdout)
        if match != None:
            return 'gst-launch-1.0' in match.group("name").strip(b'"').decode('utf-8')
        return False


#manager = WindowManager()
#print(manager.get_active_window_title())