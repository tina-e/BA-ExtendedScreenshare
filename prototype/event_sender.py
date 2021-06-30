import socket
import threading
import time
from evdev import InputDevice
from pynput.mouse import Listener, Controller
from event_types import EventTypes, get_id_by_button
import window_manager
import Config

class Sender:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        device_thread = threading.Thread(target=self.listen_device)
        device_thread.start()
        self.mouse = Controller()
        movement_thread = threading.Thread(target=self.send_mouse_pos)
        movement_thread.start()

    def send(self, message):
        self.sock.sendto(message, (Config.STREAMER_ADDRESS, Config.EVENT_PORT))

    def send_mouse_pos(self):
        while window_manager.is_in_focus():
            mouse_x = self.mouse.position[0]
            mouse_y = self.mouse.position[1]
            rel_x, rel_y = window_manager.get_pos_in_stream(mouse_x, mouse_y)
            if rel_x:
                message = EventTypes.MOUSE_MOVEMENT.to_bytes(1, 'big')
                message += rel_x.to_bytes(2, 'big')
                message += rel_y.to_bytes(2, 'big')
                self.send(message)
            time.sleep(0.1)

    def on_mouse_moved(self, x, y):
        if window_manager.is_in_focus():
            rel_x, rel_y = window_manager.get_pos_in_stream(x, y)
            if rel_x:
                message = EventTypes.MOUSE_MOVEMENT.to_bytes(1, 'big')
                message += rel_x.to_bytes(2, 'big')
                message += rel_y.to_bytes(2, 'big')
                self.send(message)

    def on_click(self, x, y, button, was_pressed):
        if window_manager.is_in_focus():
            rel_x, rel_y = window_manager.get_pos_in_stream(x, y)
            if rel_x:
                message = EventTypes.MOUSE_CLICK.to_bytes(1, 'big')
                message += rel_x.to_bytes(2, 'big')
                message += rel_y.to_bytes(2, 'big')
                message += get_id_by_button(button).to_bytes(1, 'big')
                message += was_pressed.to_bytes(1, 'big')
                self.send(message)

    def on_scroll(self, x, y, dx, dy):
        if window_manager.is_in_focus():
            rel_x, rel_y = window_manager.get_pos_in_stream(x, y)
            if rel_x:
                message = EventTypes.MOUSE_SCROLL.to_bytes(1, 'big')
                message += rel_x.to_bytes(2, 'big')
                message += rel_y.to_bytes(2, 'big')
                message += dx.to_bytes(2, 'big', signed=True)
                message += dy.to_bytes(2, 'big', signed=True)
                self.send(message)

    def listen_device(self):
        with Listener(on_click=self.on_click,
                      on_scroll=self.on_scroll) as listener:
            listener.join()
