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
        self.app.add_url_rule(f'/{Config.MOUSE_EVENT}', Config.MOUSE_EVENT, self.mouse_route, methods=['POST'])

    def start(self):
        self.app.run(host=Config.HOST, port=Config.PORT, threaded=True)

    def mouse_route(self):
        data = request.json
        print(data)
        return Response(data, mimetype='application/json')

server = Server()
server.start()
