# https://www.youtube.com/watch?v=HDY8pf-b1nA
# sudo apt install python3-gst-1.0

from streamer.stream import Stream
from streamer.mouse_handler import EventHandlerEvdev
from streamer.file_communication_streamer import FileServer
from event_types import EventTypes, get_button_by_id

import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
import socket
import threading
import subprocess
import pyautogui
import time

class Streamer:
    def __init__(self, configurator):
        self.config = configurator
        self.superior_app = QApplication(sys.argv)
        # event communication
        self.receiving = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.config.STREAMER_ADDRESS, self.config.EVENT_PORT))
        self.event_handler = EventHandlerEvdev(configurator)
        self.connection_thread_events = threading.Thread(target=self.receive, daemon=True)
        self.connection_thread_events.start()
        # file communication
        self.file_communicator = FileServer(self, self.config.FILE_EVENT, self.config.STREAMER_ADDRESS, self.config.FILE_PORT)
        connection_thread_files = threading.Thread(target=self.file_communicator.start, daemon=True)
        connection_thread_files.start()
        # shared clipboard
        self.clip_process = None
        # stream
        self.stream = Stream(configurator)
        self.is_stream_active = False

    def send_stream_coords(self):
        message = EventTypes.STREAM_COORDS.to_bytes(1, 'big')
        message += self.config.START_X.to_bytes(2, 'big')
        message += self.config.START_Y.to_bytes(2, 'big')
        message += self.config.END_X.to_bytes(2, 'big')
        message += self.config.END_Y.to_bytes(2, 'big')
        print(self.config.RECEIVER_ADDRESS)
        self.sock.sendto(message, (self.config.RECEIVER_ADDRESS, self.config.EVENT_PORT))

    def send_stream_closed(self):
        message = EventTypes.STREAM_CLOSED.to_bytes(1, 'big')
        self.sock.sendto(message, (self.config.RECEIVER_ADDRESS, self.config.EVENT_PORT))

    def receive(self):
        print("Waiting for viewer...")
        while True:
            data, addr = self.sock.recvfrom(1024)
            if not self.receiving: return
            try:
                event_type = EventTypes(data[0])
                if event_type == EventTypes.REGISTER:
                    self.config.set_receiver_ip(addr[0])
                    self.config.write_clipboard_config()
                    self.send_stream_coords()
                    self.start_stream()
                elif event_type == EventTypes.VIEWING:
                    queries_stream = data[1]
                    # print(f"is someone watching stream? {queries_stream}")
                    self.handle_view(queries_stream)
                elif self.is_stream_active:
                    if event_type == EventTypes.MOUSE_MOVEMENT:
                        event_x = int.from_bytes(data[1:3], 'big')
                        event_y = int.from_bytes(data[3:5], 'big')
                        # print(f"moved {event_x}, {event_y}")
                        self.event_handler.map_mouse_movement(event_x, event_y)
                        self.stream.on_mouse_pos_message(event_x, event_y)
                    elif event_type == EventTypes.MOUSE_CLICK:
                        event_x = int.from_bytes(data[1:3], 'big')
                        event_y = int.from_bytes(data[3:5], 'big')
                        event_button = get_button_by_id(data[5])
                        event_was_pressed = data[6]
                        # print(f"clicked at {event_x}, {event_y} with button {event_button}; pressed: {event_was_pressed}")
                        self.event_handler.map_mouse_click(event_x, event_y, event_button, event_was_pressed)
                        self.stream.on_mouse_pos_message(event_x, event_y)
                    elif event_type == EventTypes.MOUSE_SCROLL:
                        event_dx = int.from_bytes(data[5:7], 'big', signed=True)
                        event_dy = int.from_bytes(data[7:9], 'big', signed=True)
                        # print(f"scrolled {event_dx}, {event_dy}")
                        self.event_handler.map_mouse_scroll(event_dx, event_dy)
                    elif event_type == EventTypes.KEYBOARD:
                        event_key = int.from_bytes(data[1:3], 'big')
                        event_value = data[3]
                        # print(f"key {event_key}: {event_value} (down=1, up=0, hold=2)")
                        self.event_handler.map_keyboard(event_key, event_value)
            except UnicodeDecodeError:
                continue

    def handle_view(self, queries_stream):
        if queries_stream:
            self.is_stream_active = True
            self.stream.start()
            self.event_handler.create_device()
            self.clip_process = subprocess.Popen("make run", cwd=f'{self.config.PROJECT_PATH_ABSOLUTE}/clipboard',
                                                 shell=True)
        else:
            self.is_stream_active = False
            self.stream.end()
            self.event_handler.remove_device()
            self.config.clean_clipboard_config()
            self.clip_process = subprocess.Popen("make stop", cwd=f'{self.config.PROJECT_PATH_ABSOLUTE}/clipboard',
                                                 shell=True)

    def start_stream(self):
        self.stream.setup()

    def close_stream(self):
        self.receiving = False
        if self.is_stream_active:
            self.event_handler.remove_device()
            self.config.clean_clipboard_config()
            self.clip_process = subprocess.Popen("make stop", cwd=f'{self.config.PROJECT_PATH_ABSOLUTE}/clipboard', shell=True)
        self.stream.end()
        self.stream.close()
        self.file_communicator.close()
        self.is_stream_active = False

    def is_stream_open(self):
        return self.stream.is_pipeline_playing()

    def simulate_drop(self, filename, x, y):
        x_abs = self.config.START_X + int(x)
        y_abs = self.config.START_Y + int(y)
        current_x, current_y = pyautogui.position()
        path = str(self.config.PROJECT_PATH_ABSOLUTE).rsplit('/', 1)[0]
        print(path)
        subprocess.Popen(f"xcopy -D {path}/{filename}", shell=True) # todo: klappt wunderbar im FM aber außerhalb manchmal nicht?
        time.sleep(0.5) # todo?
        pyautogui.moveTo(x_abs, y_abs)
        pyautogui.mouseDown()
        time.sleep(0.5)  # todo?
        pyautogui.mouseUp()
        pyautogui.moveTo(current_x, current_y)

    def dragon_drop(self, filename, x, y):
        path = str(self.config.PROJECT_PATH_ABSOLUTE).rsplit('/', 1)[0]
        subprocess.Popen(f"dragon -x {path}/{filename}", shell=True)
        self.event_handler.simualte_drop(x, y)
##############################################################################################################################

# ! video/x-raw,width=750,height=500   legt größe des streams fest
# use-damage=0 angeblich CPU fordernd
# ximageslink creates window for output (glimagesink also possible, higher CPU required)
# pipeline = Gst.parse_launch("ximagesrc startx=100 starty=10 endx=800 endy=800 ! video/x-raw,framerate=30/1 ! ximagesink")

# pipeline = Gst.parse_launch("rtpmp4vpay ! decodebin ! videoconvert ! autovideosink")
# pipeline = Gst.parse_launch("v4l2src ! decodebin ! videoconvert ! appsink name=sink")
# appsink = pipeline.get_by_name("sink")
# pipeline.set_state(Gst.State.PLAYING)
