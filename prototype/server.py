# https://github.com/PDA-UR/Screenshotmatcher-2.0/blob/master/python-server/src/server/server.py

#import uuid
import json
#import platform
from flask import Flask, request, Response
#import common.log
import Config
import mouse_handler
#from matching.matcher import Matcher
#from common.utility import get_current_ms
from evdev import InputDevice, ecodes as e, events

class Server:
    def __init__(self):
        self.logs = []
        self.app = Flask(__name__)
        self.app.add_url_rule(f'/{Config.MOUSE_EVENT}', Config.MOUSE_EVENT, self.mouse_route, methods=['POST'])
        #mouse_handler.add_cursor()

    def start(self):
        self.app.run(host=Config.HOST, port=Config.EVENT_PORT, threaded=True)

    def cap_route(self):
        data = request.json
        mouse_data = {int(key): value for key, value in data["mouse"].items()}
        key_data = {int(key): value for key, value in data["keyboard"].items()}
        print(mouse_data)
        print(key_data)
        mouse_handler.add_cursor(mouse_data, key_data)
        return Response(data, mimetype='application/json')

    def mouse_route(self):
        data = request.json
        print(data)
        mouse_handler.map_input(data)
        return Response(data, mimetype='application/json')

