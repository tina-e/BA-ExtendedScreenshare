import time

import Config
import json
import http.client as client
from evdev import InputDevice, ecodes
from pynput.mouse import Listener
import window_manager


class Client:
    def __init__(self):
        self.connection = client.HTTPConnection(Config.HOST, Config.EVENT_PORT)
        self.mouse_device = InputDevice('/dev/input/event11')
        self.key_device = InputDevice('/dev/input/event3')

    def connect(self):
        self.connection.connect()
        self.connection.request('GET', f"http://{Config.HOST}:{Config.CAP_PORT}/connect")
        response = self.connection.getresponse()
        #self.send_device_info()

    def send_device_info(self):
        #mouse_capas = self.mouse_device.capabilities()
        #key_capas = self.key_device.capabilities()
        #print(mouse_capas)
        #print(key_capas)
        #position = window_manager.get_mouse_pos_rel_to_stream()
        #_data = json.dumps({"position": position, "mouse": mouse_capas, "keyboard": key_capas})
        headers = {'Content-type': 'application/json'}
        #self.connection.request('POST', f"http://{Config.HOST}:{Config.CAP_PORT}/{Config.CAP_EVENT}", _data, headers)
        response = self.connection.getresponse()


    def listen_on_device(self):
        if window_manager.is_in_focus():
            for event in self.mouse_device.read_loop():
            #if window_manager.is_in_focus():
                timestamp = event.timestamp()
                code = event.code
                type = event.type
                val = event.value
                _data = json.dumps({"event": str(event), "timestamp": timestamp, "code": code, "type": type, "val": val})
                headers = {'Content-type': 'application/json'}
                self.connection.request('POST', f"http://{Config.HOST}:{Config.EVENT_PORT}/{Config.MOUSE_EVENT}", _data, headers)
                response = self.connection.getresponse()

    def on_move(self, x, y):
        _data = json.dumps({"x": x, "y": y})
        headers = {'Content-type': 'application/json'}
        self.connection.request('POST', f"http://{Config.HOST}:{Config.EVENT_PORT}/{Config.MOUSE_EVENT}", _data, headers)
        response = self.connection.getresponse()

    def listen_on_device_abs(self):
        with Listener(on_move=self.on_move) as listener:
            listener.join()
