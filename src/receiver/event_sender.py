import selectors
import socket
import subprocess
import threading
import time
import pyclip

# import gi
# gi.require_version('Gtk', '3.0')
# from gi.repository import Gtk, Gdk
from evdev import InputDevice, ecodes
from pynput.mouse import Listener as MouseListener, Controller as MouseController
from event_types import EventTypes, get_id_by_button


class EventSender:
    '''
    EventSender listens for input events and sends them to the streamer via UDP-Socket.
    '''
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
        self.ctr_hold = False

    def start_event_listeners(self):
        self.button_thread.start()
        self.movement_thread.start()
        self.keyboard_thread.start()

    def register(self):
        '''
        Registers the receiver on the streamer.
        If receiver cant find an active stream at the given IP, he will try again up to four times.
        If there is still no stream to find, the action is cancelled.
        If a attempt was successfull, the receiver waits for the stream coordinates to open the stream-window.
        :return: stream found?
        '''
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
        else:
            self.active = False
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
                    # print("CLICK", message)
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
                    # print("SCROLL", message)
                    self.send(message)

    def listen_mouse_pos(self):
        '''
        sends (updated) current mouse-position every 100ms
        :return:
        '''
        while self.active:
            if self.stream_window.is_active():
                mouse_x = self.mouse.position[0]
                mouse_y = self.mouse.position[1]
                x_in_stream, y_in_stream = self.stream_window.get_position_in_stream(mouse_x, mouse_y)
                if x_in_stream:
                    message = EventTypes.MOUSE_MOVEMENT.to_bytes(1, 'big')
                    message += x_in_stream.to_bytes(2, 'big')
                    message += y_in_stream.to_bytes(2, 'big')
                    # print("POINT", message)
                    self.send(message)
            time.sleep(0.1)

    def listen_keyboard(self):
        '''
        Forwards all keyboard events, but CTRL+C and CTRL+V.
        Copy-actions or paste-actions require other actions.
        '''
        for event in self.keyboard.read_loop():
            if self.active:
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
                                self.on_remote_paste()
                            elif event.code == 46 and event.value == 1:
                                print("ctr-c pressed")
                                self.on_remote_copy()
                        else:
                            message = EventTypes.KEYBOARD.to_bytes(1, 'big')
                            message += event.code.to_bytes(2, 'big')  # key
                            message += event.value.to_bytes(1, 'big')  # down = 1, up = 0, hold = 2
                            # print("KEY", message)
                            self.send(message)

    def on_remote_paste(self):
        '''
        By typing CTRL+V inside the stream-window,
        the local clipboard content is sent to the streamer.
        It will be pasted there.
        '''
        current_local_cb_content = pyclip.paste()
        print(current_local_cb_content)
        message = EventTypes.PASTE.to_bytes(1, 'big')
        message += current_local_cb_content
        self.send(message)

    def on_remote_copy(self):
        '''
        By typing CTRL+C inside the stream-window,
        the streamer gets informed that the receiver wants to copy the selected content.
        A thread for receiving the copied content is started.
        '''
        clipboard_content_thread = threading.Thread(target=self.receive_clip_content)
        clipboard_content_thread.start()
        message = EventTypes.COPY.to_bytes(1, 'big')
        self.send(message)

    def receive_clip_content(self):
        '''
        Socket receives the selected content.
        The received text is copied to the local clipboard and can now be pasted as usual.
        '''
        clip_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clip_sock.bind((self.config.RECEIVER_ADDRESS, self.config.EVENT_PORT))
        waiting_for_answer = True
        while waiting_for_answer:
            print("receiving clip")
            data, addr = clip_sock.recvfrom(1024)
            print(data)
            try:
                event_type = EventTypes(data[0])
                if event_type == EventTypes.COPY:
                    received_clipboard_content = data[1:].decode('utf-8')
                    print(received_clipboard_content)
                    pyclip.copy(received_clipboard_content)
                    waiting_for_answer = False
            except UnicodeDecodeError:
                continue
        clip_sock.close()
