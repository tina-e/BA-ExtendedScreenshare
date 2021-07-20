import ctypes
import os
import threading
import time

import Config


class FrameMaker:
    def __init__(self):
        self.frame = ctypes.CDLL("/home/martinaemmert/Documents/Bachelorarbeit/CrossDeviceCommunication/prototype/streamer/libframe.so")
        self.frame.setup.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.frame.draw.argtypes = [ctypes.c_int]
        self.frame.setup(Config.START_X, Config.START_Y, Config.END_X, Config.END_Y)
        self.is_visible = False
        self.drawing_thread = threading.Thread(target=self.__draw, daemon=True)
        self.drawing_thread.start()

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


