import ctypes
import os
import threading


class CHandler:
    def __init__(self, x, y, width, height):
        self.frame = ctypes.CDLL("./libframe.so")
        self.frame.setup.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.frame.setup(x, y, width, height)
        self.drawing_thread = threading.Thread(target=self.draw, daemon=True)

    def show_frame(self):
        self.drawing_thread.start()

    def draw(self):
        while True:
            self.frame.draw()

    def end_frame(self):
        print("end")
        self.frame.end()
        exit(0)





