import socket
import threading
import time
from evdev import InputDevice
from pynput.mouse import Listener
from event_types import EventTypes
import window_manager
import Config

class Sender:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.mouse_device = InputDevice('/dev/input/event11')
        self.key_device = InputDevice('/dev/input/event3')
        device_thread = threading.Thread(target=self.listen_device)
        device_thread.start()

    def send(self, message):
        self.sock.sendto(message, (Config.STREAMER_ADDRESS, Config.EVENT_PORT))

    def on_mouse_moved(self, x, y):
        rel_x, rel_y = window_manager.get_pos_rel_to_stream(x, y)
        message_array = [EventTypes.MOUSE_MOVEMENT, rel_x, rel_y]
        self.send(bytearray(message_array))

    def listen_device(self):
        with Listener(on_move=self.on_mouse_moved) as listener:
            listener.join()
