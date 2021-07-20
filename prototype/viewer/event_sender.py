import selectors
import socket
import threading
import time
from evdev import InputDevice, ecodes, categorize
from pynput.mouse import Listener as MouseListener, Controller as MouseController
from pynput.keyboard import Key, Listener as KeyListener, Controller as KeyController
from event_types import EventTypes, get_id_by_button
import window_manager
from window_manager_test import WindowManager
import Config


class EventSender:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mouse = MouseController()  # self.keyboard = KeyController()
        #self.mouse = InputDevice('/dev/input/event12')
        self.keyboard = InputDevice('/dev/input/event3')

        button_thread = MouseListener(on_click=self.on_click, on_scroll=self.on_scroll)
        button_thread.daemon = True
        button_thread.start()

        # todo: manchmal immer noch absturz, threading?
        #  xlib.threaded nutzen aber nicht möglich, da in allen bibliotheken benutzt
        movement_thread = threading.Thread(target=self.listen_mouse_pos, daemon=True)
        movement_thread.start()

        keyboard_thread = threading.Thread(target=self.listen_keyboard, daemon=True)
        keyboard_thread.start()


    def send(self, message):
        self.sock.sendto(message, (Config.STREAMER_ADDRESS, Config.EVENT_PORT))

    def on_view(self, is_viewing):
        message = EventTypes.VIEWING.to_bytes(1, 'big')
        message += is_viewing.to_bytes(1, 'big')
        print(message)
        self.send(message)
        #window_manager.setup()

    def on_click(self, x, y, button, was_pressed):
        if window_manager.is_in_focus():
            rel_x, rel_y = window_manager.get_pos_in_stream(x, y)
            if rel_x:
                message = EventTypes.MOUSE_CLICK.to_bytes(1, 'big')
                message += rel_x.to_bytes(2, 'big')
                message += rel_y.to_bytes(2, 'big')
                message += get_id_by_button(button).to_bytes(1, 'big')
                message += was_pressed.to_bytes(1, 'big')
                print(message)
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
                print(message)
                self.send(message)

    def listen_mouse_pos(self):
        while True:
            if window_manager.is_in_focus():
                mouse_x = self.mouse.position[0]
                mouse_y = self.mouse.position[1]
                rel_x, rel_y = window_manager.get_pos_in_stream(mouse_x, mouse_y)
                if rel_x:
                    message = EventTypes.MOUSE_MOVEMENT.to_bytes(1, 'big')
                    message += rel_x.to_bytes(2, 'big')
                    message += rel_y.to_bytes(2, 'big')
                    print("POINT", message)
                    self.send(message)
            time.sleep(0.1)

    def listen_keyboard(self):
        for event in self.keyboard.read_loop():
            if window_manager.is_in_focus():
                if event.type == ecodes.EV_KEY:
                    message = EventTypes.KEYBOARD.to_bytes(1, 'big')
                    message += event.code.to_bytes(2, 'big')  # key
                    message += event.value.to_bytes(1, 'big')  # down = 1, up = 0, hold = 2
                    print("KEY", message)
                    self.send(message)

    ###################################################################################################################

    def listen_device(self):
        # todo: cannot read absolute postitons with evdev??
        selector = selectors.DefaultSelector()
        selector.register(self.mouse, selectors.EVENT_READ)
        selector.register(self.keyboard, selectors.EVENT_READ)
        while True:
            for k, m in selector.select():
                device = k.fileobj
                for event in device.read():
                    print(event)

    # too much delay
    def on_mouse_moved(self, x, y):
        if window_manager.is_in_focus():
            rel_x, rel_y = window_manager.get_pos_in_stream(x, y)
            if rel_x:
                message = EventTypes.MOUSE_MOVEMENT.to_bytes(1, 'big')
                message += rel_x.to_bytes(2, 'big')
                message += rel_y.to_bytes(2, 'big')
                self.send(message)
