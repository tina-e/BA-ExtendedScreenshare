# https://github.com/PDA-UR/Screenshotmatcher-2.0/blob/master/python-server/src/server/server.py

#import uuid
import json
#import platform
from flask import Flask, request, Response
#import common.log
import Config_alt
from mouse_handler import EventHandlerEvdev
#from matching.matcher import Matcher
#from common.utility import get_current_ms
from evdev import InputDevice, ecodes as e, events

class Server:
    def __init__(self):
        self.logs = []
        self.app = Flask(__name__)
        self.client_pointer = None
        self.app.add_url_rule("/connect", "connect", self.connect_route)
        self.app.add_url_rule(f'/{Config_alt.CAP_EVENT}', Config_alt.CAP_EVENT, self.cap_route_rel, methods=['POST'])
        self.app.add_url_rule(f'/{Config_alt.MOUSE_EVENT}', Config_alt.MOUSE_EVENT, self.mouse_route, methods=['POST'])
        #self.app.add_url_rule(f'/{Config.MOUSE_EVENT}', Config.MOUSE_EVENT, self.mouse_route_abs, methods=['POST'])

    def start(self):
        self.app.run(host=Config_alt.STREAMER_ADDRESS, port=Config_alt.EVENT_PORT, threaded=True)

    def connect_route(self):
        self.client_pointer = EventHandlerEvdev()
        print("Client connected to server")

    def cap_route_rel(self):
        data = request.json
        position_data = data["position"]
        mouse_data = {int(key): tuple(value) for key, value in data["mouse"].items()}
        key_data = {int(key): tuple(value) for key, value in data["keyboard"].items()}
        print(mouse_data)
        print(key_data)
        return Response(data, mimetype='application/json')

    def mouse_route(self):
        data = request.json
        print(data)
        self.client_pointer.map_input(data)
        return Response(data, mimetype='application/json')

    def mouse_route_abs(self):
        data = request.json
        print(data)
        self.client_pointer.map_input_abs(data)
        return Response(data, mimetype='application/json')

