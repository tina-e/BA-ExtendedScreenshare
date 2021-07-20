import ctypes
import os
import threading
import time

import Config


class FrameMaker:
    def __init__(self):
        print("start frame maker")
        self.frame = ctypes.CDLL("/home/tina/PycharmProjects/BA-CrossDeviceCommunication/prototype/streamer/libframe.so")
        self.frame.setup.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.frame.setup(Config.START_X, Config.START_Y, Config.END_X, Config.END_Y)
        self.is_visible = False
        print("start drawing loop")
        self.drawing_thread = threading.Thread(target=self.__draw, daemon=True)
        self.drawing_thread.start()

    def toggle_visibility(self):
        self.is_visible = not self.is_visible
        print("toggle visibility:", self.is_visible)

    def __draw(self):
        while True:
            time.sleep(1)
            print("visibility:", self.is_visible)
            if self.is_visible:
                pass
                # self.frame.draw()

    def end(self):
        self.is_visible = False
        self.frame.end()

#frame = Frame()
#frame.setup()
#frame.show()


