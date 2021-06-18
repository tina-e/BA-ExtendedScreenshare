import time

import Config
import json
import http.client as client
from evdev import InputDevice, ecodes
from pynput.mouse import Button, Controller
from ewmh import EWMH
ewmh = EWMH()

class Client:
    def __init__(self):
        self.connection = client.HTTPConnection(Config.HOST, Config.EVENT_PORT)
        self.mouse_device = InputDevice('/dev/input/event11')
        self.key_device = InputDevice('/dev/input/event3')

    def connect(self):
        self.connection.connect()
        self.send_device_info()

    def send_device_info(self):
        mouse_capas = self.mouse_device.capabilities()
        key_capas = self.key_device.capabilities()
        print(mouse_capas)
        print(key_capas)
        position = get_position()
        _data = json.dumps({"position": position, "mouse": mouse_capas, "keyboard": key_capas})
        headers = {'Content-type': 'application/json'}
        self.connection.request('POST', f"http://{Config.HOST}:{Config.CAP_PORT}/{Config.CAP_EVENT}", _data, headers)
        response = self.connection.getresponse()


    def listen_on_device(self):
        for event in self.mouse_device.read_loop():
            #if is_relevant_input():
            timestamp = event.timestamp()
            code = event.code
            type = event.type
            val = event.value
            _data = json.dumps({"event": str(event), "timestamp": timestamp, "code": code, "type": type, "val": val})
            headers = {'Content-type': 'application/json'}
            self.connection.request('POST', f"http://{Config.HOST}:{Config.EVENT_PORT}/{Config.MOUSE_EVENT}", _data, headers)
            response = self.connection.getresponse()


def is_relevant_input():
    window = ewmh.getActiveWindow()
    if window.get_wm_class() == ('gst-launch-1.0', 'GStreamer'):
        mouse_pos = Controller().position
        win_geo = frame(window).get_geometry()
        if (win_geo.x <= mouse_pos[0] <= (win_geo.width + win_geo.x)) and (win_geo.y <= mouse_pos[1] <= (win_geo.height + win_geo.y)):
            return True
    return False


def frame(window):
    framed_window = window
    while framed_window.query_tree().parent != ewmh.root:
        framed_window = framed_window.query_tree().parent
    return framed_window


def get_position():
    win_geo = None
    mouse_pos = Controller().position
    open_wins = ewmh.getClientList()
    for win in open_wins:
        if win.get_wm_class() == ('gst-launch-1.0', 'GStreamer'):
            win_geo = frame(win).get_geometry()
            break
    return mouse_pos[0] - win_geo.x, mouse_pos[1] - win_geo.y


