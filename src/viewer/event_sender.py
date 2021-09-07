import selectors
import socket
import subprocess
import threading
import time

# import gi
# gi.require_version('Gtk', '3.0')
# from gi.repository import Gtk, Gdk
from evdev import InputDevice, ecodes
from pynput.mouse import Listener as MouseListener, Controller as MouseController
from event_types import EventTypes, get_id_by_button


class EventSender:
    def __init__(self, stream_window, configurator):
        self.stream_window = stream_window
        self.config = configurator
        self.active = False

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.mouse = MouseController()
        self.keyboard = InputDevice(self.config.KEYBOARD_DEVICE_PATH)

        self.button_thread = MouseListener(on_click=self.on_click, on_scroll=self.on_scroll)
        self.button_thread.daemon = True
        self.movement_thread = threading.Thread(target=self.listen_mouse_pos, daemon=True)
        self.keyboard_thread = threading.Thread(target=self.listen_keyboard, daemon=True)

        self.clip_process = None
        #self.ctr_hold = False

    def start_event_listeners(self):
        self.button_thread.start()
        self.movement_thread.start()
        self.keyboard_thread.start()

    def register(self):
        message = EventTypes.REGISTER.to_bytes(1, 'big')
        attempts = 5
        for attempt in range(0, attempts):
            # print("REGISTER", message)
            self.sock.sendto(message, (self.config.STREAMER_ADDRESS, self.config.EVENT_PORT))

            receiving_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            receiving_sock.bind((self.config.RECEIVER_ADDRESS, self.config.EVENT_PORT))
            receiving_sock.settimeout(1)
            try:
                data, addr = receiving_sock.recvfrom(1024)
                try:
                    event_type = EventTypes(data[0])
                    if event_type == EventTypes.STREAM_COORDS:
                        x = int.from_bytes(data[1:3], 'big')
                        y = int.from_bytes(data[3:5], 'big')
                        end_x = int.from_bytes(data[5:7], 'big')
                        end_y = int.from_bytes(data[7:9], 'big')
                        self.config.set_coords((x, y, end_x, end_y))
                        receiving_sock.close()
                        return True
                except UnicodeDecodeError:
                    continue
            except socket.timeout:
                receiving_sock.close()
                print("Currently no stream available. Trying again in a second...")
                time.sleep(1)
        print("No stream available at the given IP")
        return False

    def send(self, message):
        self.sock.sendto(message, (self.config.STREAMER_ADDRESS, self.config.EVENT_PORT))

    def on_view(self, is_viewing):
        if is_viewing:
            self.active = True
            self.start_event_listeners()
            self.clip_process = subprocess.Popen("make run", cwd=f'{self.config.PROJECT_PATH_ABSOLUTE}/clipboard', shell=True)
        else:
            self.active = False
            self.clip_process = subprocess.Popen("make stop", cwd=f'{self.config.PROJECT_PATH_ABSOLUTE}/clipboard', shell=True)
        message = EventTypes.VIEWING.to_bytes(1, 'big')
        message += is_viewing.to_bytes(1, 'big')
        # print("VIEW", message)
        self.send(message)

    def on_click(self, x, y, button, was_pressed):
        if self.active:
            if self.stream_window.is_active():
                x_in_stream, y_in_stream = self.stream_window.get_position_in_stream(x, y)
                if x_in_stream:
                    message = EventTypes.MOUSE_CLICK.to_bytes(1, 'big')
                    message += x_in_stream.to_bytes(2, 'big')
                    message += y_in_stream.to_bytes(2, 'big')
                    message += get_id_by_button(button).to_bytes(1, 'big')
                    message += was_pressed.to_bytes(1, 'big')
                    #print("CLICK", message)
                    self.send(message)

    def on_scroll(self, x, y, dx, dy):
        if self.active:
            if self.stream_window.is_active():
                x_in_stream, y_in_stream = self.stream_window.get_position_in_stream(x, y)
                if x_in_stream:
                    message = EventTypes.MOUSE_SCROLL.to_bytes(1, 'big')
                    message += x_in_stream.to_bytes(2, 'big')
                    message += y_in_stream.to_bytes(2, 'big')
                    message += dx.to_bytes(2, 'big', signed=True)
                    message += dy.to_bytes(2, 'big', signed=True)
                    #print("SCROLL", message)
                    self.send(message)

    def listen_mouse_pos(self):
        while self.active:
            if self.stream_window.is_active(): #todo
                mouse_x = self.mouse.position[0]
                mouse_y = self.mouse.position[1]
                x_in_stream, y_in_stream = self.stream_window.get_position_in_stream(mouse_x, mouse_y)
                if x_in_stream:
                    message = EventTypes.MOUSE_MOVEMENT.to_bytes(1, 'big')
                    message += x_in_stream.to_bytes(2, 'big')
                    message += y_in_stream.to_bytes(2, 'big')
                    #print("POINT", message)
                    self.send(message)
            time.sleep(0.1)

    def listen_keyboard(self):
        for event in self.keyboard.read_loop():
            if self.active:
                if self.stream_window.is_active():
                    if event.type == ecodes.EV_KEY:
                        message = EventTypes.KEYBOARD.to_bytes(1, 'big')
                        message += event.code.to_bytes(2, 'big')  # key
                        message += event.value.to_bytes(1, 'big')  # down = 1, up = 0, hold = 2
                        #print("KEY", message)
                        self.send(message)

    '''if event.code == 29:
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
    else:'''

    '''def on_paste(self):
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
        return'''


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
