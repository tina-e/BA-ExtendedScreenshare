import ctypes
import os
import threading
import time

import Config


class FrameMaker:
    def __init__(self):
        self.frame = ctypes.CDLL("/home/martinaemmert/Documents/Bachelorarbeit/CrossDeviceCommunication/prototype/streamer/libframe.so")
        self.frame.setup.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.frame.draw.argtypes = [ctypes.c_int]
        x, y, width, height = self.get_frame_position()
        self.frame.setup(x, y, width, height, Config.BORDER_WIDTH)
        self.is_visible = False
        self.drawing_thread = threading.Thread(target=self.__draw, daemon=True)
        self.drawing_thread.start()

    def get_frame_position(self):
        #todo: dragable area
        frame_x = Config.START_X - Config.BORDER_WIDTH
        frame_y = Config.START_Y - Config.BORDER_WIDTH
        frame_width = Config.WIDTH + 2 * Config.BORDER_WIDTH
        frame_height = Config.HEIGHT + 2 * Config.BORDER_WIDTH
        if frame_x <= 0:
            frame_x = 0
        if frame_y <= 0:
            frame_y = 0
        if frame_width + frame_x > Config.RESOLUTION_X:
            frame_width = Config.RESOLUTION_X - frame_x
        if frame_height + frame_y > Config.RESOLUTION_Y:
            frame_height = Config.RESOLUTION_Y - frame_y
        return frame_x, frame_y, frame_width, frame_height

    def toggle_visibility(self):
        self.is_visible = not self.is_visible

    def __draw(self):
        while True:
            time.sleep(1)
            if self.is_visible:
                self.frame.draw(1)
            else:
                self.frame.draw(0)

    def end(self):
        self.is_visible = False
        self.frame.end()

#frame = Frame()
#frame.setup()
#frame.show()


