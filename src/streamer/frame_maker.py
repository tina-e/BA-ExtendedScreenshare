import ctypes
import threading
import time


class FrameMaker:
    '''
    This class uses a self-written C-Library to draw a frame for marking the shared region.
    Also a dot is drawn which follows the receiver's cursor, so you can differ the two existing cursors.
    '''
    def __init__(self, x, y, width, height, border_width, max_width, max_height, project_path):
        self.border_width = border_width
        self.max_width = max_width
        self.max_height = max_height
        self.x, self.y, self.width, self.height = self.get_frame_position(x, y, width, height)

        self.frame = ctypes.CDLL(f"{project_path}/streamer/libframe.so")
        self.frame.setup_rect.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.frame.draw.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.frame.setup_rect(self.x, self.y, self.width, self.height, self.border_width)

        self.is_visible = False
        self.mouse_x = self.x
        self.mouse_y = self.y
        self.drawing_thread = threading.Thread(target=self.draw, daemon=True)
        self.drawing_thread.start()

    def get_frame_position(self, x, y, width, height):
        '''
        Makes sure, the frame is not outside the screen.
        Provides the receiver from seeing the frame
        by setting the coordinates for the frame outside the streamed area.
        '''
        frame_x = x - self.border_width
        frame_y = y - self.border_width
        frame_width = width + 2 * self.border_width
        frame_height = height + 2 * self.border_width
        if frame_x <= 0:
            frame_x = 0
        if frame_y <= 0:
            frame_y = 0
        if frame_width + frame_x > self.max_width:
            frame_width = self.max_width - frame_x
        if frame_height + frame_y > self.max_height:
            frame_height = self.max_height - frame_y
        return frame_x, frame_y, frame_width, frame_height

    def set_mouse_pos(self, mouse_x, mouse_y):
        '''
        Maps the red dot to the mouse cursor.
        :param mouse_x: x_pos of receiver's cursor
        :param mouse_y: y_pos pf receiver's cursor
        '''
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

    def toggle_visibility(self):
        '''
        Represents if someone is watching the stream
        -> the color of the frame will change from grey to red if someone is watching
        '''
        self.is_visible = not self.is_visible

    def draw(self):
        while True:
            time.sleep(0.05)
            if self.is_visible:
                self.frame.draw(1, self.mouse_x, self.mouse_y)
            else:
                self.frame.draw(0, self.mouse_x, self.mouse_y)

    def end(self):
        self.is_visible = False
        self.frame.end()
