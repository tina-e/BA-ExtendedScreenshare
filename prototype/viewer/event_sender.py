import selectors
import socket
import threading
import time

import gi
import pyautogui
from evdev import InputDevice, ecodes, categorize
from pynput.mouse import Listener as MouseListener, Controller as MouseController
import pyperclip
from tkinter import Tk
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from pynput.keyboard import Key, Listener as KeyListener, Controller as KeyController
from event_types import EventTypes, get_id_by_button
import window_manager
#from window_manager_test import WindowManager
import Config

class EventSender:
    def __init__(self, stream_window):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mouse = MouseController()  # self.keyboard = KeyController()
        #self.mouse = InputDevice('/dev/input/event12')
        self.keyboard = InputDevice('/dev/input/event3')
        self.stream_window = stream_window

        #self.tk = Tk()
        self.ctr_hold = False

        button_thread = MouseListener(on_click=self.on_click, on_scroll=self.on_scroll)
        button_thread.daemon = True
        button_thread.start()

        movement_thread = threading.Thread(target=self.listen_mouse_pos, daemon=True)
        movement_thread.start()

        keyboard_thread = threading.Thread(target=self.listen_keyboard, daemon=True)
        keyboard_thread.start()


    def send(self, message):
        self.sock.sendto(message, (Config.STREAMER_ADDRESS, Config.EVENT_PORT))

    def on_view(self, is_viewing):
        message = EventTypes.VIEWING.to_bytes(1, 'big')
        message += is_viewing.to_bytes(1, 'big')
        print("VIEW", message)
        self.send(message)

    def on_click(self, x, y, button, was_pressed):
        if self.stream_window.is_active():
            x_in_stream, y_in_stream = self.stream_window.get_position_in_stream(x, y)
            if x_in_stream:
                message = EventTypes.MOUSE_CLICK.to_bytes(1, 'big')
                message += x_in_stream.to_bytes(2, 'big')
                message += y_in_stream.to_bytes(2, 'big')
                message += get_id_by_button(button).to_bytes(1, 'big')
                message += was_pressed.to_bytes(1, 'big')
                print("CLICK", message)
                self.send(message)

    def on_scroll(self, x, y, dx, dy):
        if self.stream_window.is_active():
            x_in_stream, y_in_stream = self.stream_window.get_position_in_stream(x, y)
            if x_in_stream:
                message = EventTypes.MOUSE_SCROLL.to_bytes(1, 'big')
                message += x_in_stream.to_bytes(2, 'big')
                message += y_in_stream.to_bytes(2, 'big')
                message += dx.to_bytes(2, 'big', signed=True)
                message += dy.to_bytes(2, 'big', signed=True)
                print("SCROLL", message)
                self.send(message)

    def listen_mouse_pos(self):
        while True:
            if self.stream_window.is_active():
                mouse_x = self.mouse.position[0]
                mouse_y = self.mouse.position[1]
                x_in_stream, y_in_stream = self.stream_window.get_position_in_stream(mouse_x, mouse_y)
                if x_in_stream:
                    message = EventTypes.MOUSE_MOVEMENT.to_bytes(1, 'big')
                    message += x_in_stream.to_bytes(2, 'big')
                    message += y_in_stream.to_bytes(2, 'big')
                    print("POINT", message)
                    self.send(message)
            time.sleep(0.1)

    def listen_keyboard(self):
        for event in self.keyboard.read_loop():
            if self.stream_window.is_active():
                if event.type == ecodes.EV_KEY:
                  if event.code == 29:
                      if event.value == 1:
                          self.ctr_hold = True
                      elif event.value == 0:
                          self.ctr_hold = False

                  if self.ctr_hold:
                      if event.code == 47 and event.value == 1:
                          print(self.ctr_hold)
                          print("ctr-v pressed")
                          self.on_paste()
                          #continue
                      elif event.code == 46 and event.value == 1:
                          print("ctr-c pressed")
                          self.on_copy()
                          #continue
                  else:
                    message = EventTypes.KEYBOARD.to_bytes(1, 'big')
                    message += event.code.to_bytes(2, 'big')  # key
                    message += event.value.to_bytes(1, 'big')  # down = 1, up = 0, hold = 2
                    print("KEY", message)
                    self.send(message)


    def on_paste(self):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        content = clipboard.wait_for_text()
        print(content)
        message = EventTypes.PASTE.to_bytes(1, 'big')
        message += bytes(content, 'utf-8')
        print("PASTE", message)
        self.send(message)

    def on_copy(self):
        #todo:
        # aktuelle auswahl (von richtigem eingabegerät) anfordern ODER remote ctrl+c abfangen und zwei zwischenablagen bauen
        # received content in zwischenablage lokal speichern
        return

'''sen = EventSender()
while True:
    time.sleep(0.01)'''


###################################################################################################################

def listen_device(self):
    # cannot read absolute postitons with evdev??
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
