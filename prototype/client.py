import Config
import json
import http.client as client
from evdev import ecodes
from pynput.mouse import Button, Controller
from ewmh import EWMH
ewmh = EWMH()

class Client:
    def __init__(self):
        self.connection = client.HTTPConnection(Config.HOST, Config.EVENT_PORT)

    def connect(self):
        self.connection.connect()

    def listen_on_device(self, device):
        for event in device.read_loop():
            if is_relevant_input():
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
