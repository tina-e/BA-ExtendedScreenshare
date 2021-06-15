# https://github.com/PDA-UR/Screenshotmatcher-2.0/blob/master/python-server/src/server/server.py

#import uuid
import json
#import platform
from flask import Flask, request, Response
#import common.log
import Config
#from matching.matcher import Matcher
#from common.utility import get_current_ms
from evdev import InputDevice, ecodes as e, events

class Server:
    def __init__(self):
        self.logs = []
        self.app = Flask(__name__)
        self.app.add_url_rule('/mouseevent', 'mouseevent', self.mouse_route)

    def start(self):
        self.app.run(host=Config.HOST, port=Config.PORT, threaded=True)

    def mouse_route(self):
        # listen to mouse
        device = InputDevice('/dev/input/event11')
        print(device)
        for event in device.read_loop():
            timestamp = event.timestamp()
            code = event.code
            type = event.type
            val = event.value
            _data = json.dumps({"event": str(event), "timestamp": timestamp, "code": code, "type": type, "val": val})
            return Response(_data, mimetype='application/json')

server = Server()
server.start()
