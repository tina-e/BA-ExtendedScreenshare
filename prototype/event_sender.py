import socket
import threading
import time
from evdev import InputDevice, ecodes, categorize
from pynput.mouse import Listener as MouseListener, Controller as MouseController
from pynput.keyboard import Key, Listener as KeyListener, Controller as KeyController
from event_types import EventTypes, get_id_by_button
import window_manager
import Config


class Sender:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.mouse = MouseController()  # self.keyboard = KeyController()
        self.keyboard = InputDevice('/dev/input/event3')
        movement_thread = threading.Thread(target=self.listen_mouse_pos)
        movement_thread.start()
        keyboard_thread = threading.Thread(target=self.listen_keyboard)
        keyboard_thread.start()
        # button_thread = threading.Thread(target=self.listen_mouse_buttons)
        # button_thread.start() #TODO: Fehlermeldung beim Scrollen
        self.listen_mouse_buttons()

    def send(self, message):
        self.sock.sendto(message, (Config.STREAMER_ADDRESS, Config.EVENT_PORT))

    def listen_mouse_pos(self):
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

    def listen_mouse_buttons(self):
        with MouseListener(on_click=self.on_click, on_scroll=self.on_scroll) as mouse_listener:
            # KeyListener(on_press=self.on_press, on_release=self.on_release) as key_listener
            mouse_listener.join()
            # key_listener.join()

    def listen_keyboard(self):
        for event in self.keyboard.read_loop():
            if window_manager.is_in_focus():
                if event.type == ecodes.EV_KEY:
                    message = EventTypes.KEYBOARD.to_bytes(1, 'big')
                    message += event.code.to_bytes(2, 'big')  # key
                    message += event.value.to_bytes(1, 'big')  # down=1, up=0, hold=2
                    self.send(message)

    ###################################################################################################################

    def on_mouse_moved(self, x, y):
        if window_manager.is_in_focus():
            rel_x, rel_y = window_manager.get_pos_in_stream(x, y)
            if rel_x:
                message = EventTypes.MOUSE_MOVEMENT.to_bytes(1, 'big')
                message += rel_x.to_bytes(2, 'big')
                message += rel_y.to_bytes(2, 'big')
                self.send(message)

    def on_press(self, key):
        print(key)
        # if window_manager.is_in_focus():
        message = EventTypes.KEYBOARD.to_bytes(1, 'big')
        message += key.to_bytes(2, 'big')
        message += True.to_bytes(1, 'big')
        print(message)
        print("-----")
        # self.send(message)

    def on_release(self, key):
        print(key)
        # if window_manager.is_in_focus():
        message = EventTypes.KEYBOARD.to_bytes(1, 'big')
        message += key.to_bytes(2, 'big')
        message += False.to_bytes(1, 'big')
        print(message)
        print("-----")
        # self.send(message)hallooo
