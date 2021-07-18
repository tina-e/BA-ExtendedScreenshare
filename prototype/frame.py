import ctypes
import os
import threading
import time

import Config


class Frame:
    def __init__(self):
        self.frame = ctypes.CDLL("/home/martinaemmert/Documents/Bachelorarbeit/CrossDeviceCommunication/prototype/libframe.so")
        self.frame.setup.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.is_visible = False
        self.drawing_thread = threading.Thread(target=self.__draw)

    def setup(self):
        self.frame.setup(Config.START_X, Config.START_Y, Config.END_X, Config.END_Y)

    def show(self):
        self.is_visible = True
        self.drawing_thread.start()

    def __draw(self):
        while True:
            if self.is_visible:
                self.frame.draw()

    def end(self):
        self.is_visible = False
        self.frame.end()

#frame = Frame()
#frame.setup()
#frame.show()


