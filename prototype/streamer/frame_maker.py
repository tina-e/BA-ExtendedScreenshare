import ctypes
import os
import threading
import time

import Config


class FrameMaker:
    def __init__(self, event_handler):
        self.event_handler = event_handler
        self.frame = ctypes.CDLL("/home/martinaemmert/Documents/Bachelorarbeit/CrossDeviceCommunication/prototype/streamer/libframe.so")
        self.frame.setup_rect.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.frame.draw.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        #x, y, width, height = self.get_frame_position()
        #self.frame.setup_rect(x, y, width, height, Config.BORDER_WIDTH)
        self.frame.setup_rect(Config.START_X, Config.START_Y, Config.WIDTH, Config.HEIGHT, Config.BORDER_WIDTH)
        self.is_visible = False
        self.mouse_x = Config.START_X
        self.mouse_y = Config.START_Y
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

    def set_mouse_pos(self, mouse_x, mouse_y):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

    def toggle_visibility(self):
        self.is_visible = not self.is_visible

    def __draw(self):
        while True:
            time.sleep(0.1)
            if self.is_visible:
                self.frame.draw(1, self.mouse_x, self.mouse_y)
            else:
                self.frame.draw(0, self.mouse_x, self.mouse_y)

    def end(self):
        self.is_visible = False
        self.frame.end()

#frame = Frame()
#frame.setup()
#frame.show()


